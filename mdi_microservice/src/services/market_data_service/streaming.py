import json
import websocket
from websocket import create_connection
import pandas as pd
import pprint
from src.utils.utils import get_envar

def extract_ohlcv(source):
  event_time = pd.to_datetime(source['data']['E'], unit='ms')
  open = source['data']['k']['o']
  high = source['data']['k']['h']
  low = source['data']['k']['l']
  close = source['data']['k']['c']
  volume = source['data']['k']['v']

  data = {
      'open':open,
      'high':high,
      'low':low,
      'close':close,
      'volume':volume
  }

  df = pd.DataFrame(data, index=[event_time])
  df.index.name = 'timestamp'
  df = df.astype(float)
  df = df.reset_index()
  print(df)
  return df

def on_message(ws, message):
  message = json.loads(message)
  extract_ohlcv(message)

def stream_alpaca(coin):
    ALPACA_API_KEY = get_envar.get('ALPACA_API_KEY')
    ALPACA_SECRET_KEY = get_envar.get('ALPACA_SECRET_KEY')
    socket = 'wss://stream.data.alpaca.markets/v1beta3/crypto/us'
    auth_message = {"action":"auth","key": ALPACA_API_KEY, "secret": ALPACA_SECRET_KEY}
    subscription = {"action":"subscribe","bars":["BTC/USD"]}
    ws = create_connection(socket)
    ws.send(json.dumps(auth_message))
    ws.send(json.dumps(subscription))

def stream_binance(coin):
    coin = 'btcusdt@kline_1m'
    socket = 'wss://stream.binance.com:9443/stream?streams='+coin
    print(socket)
    ws = websocket.WebSocketApp(socket, on_message=on_message)
    ws.run_forever()
    return ws

# while True:
#     ws = stream_alpaca('BTC-USD')
#     ws = stream_binance('BTC-USD')
#     data = json.loads(ws.recv())
#     pprint.pprint(data[0])