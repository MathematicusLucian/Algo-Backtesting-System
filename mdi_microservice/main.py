from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
from src.services.strategy.macd import MACD
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
plt.style.use('fivethirtyeight')

base="USD"
second_currency="BTC"
period="1yr"
fast=12
slow=26
signal=9
ta_sample_data = "./src/services/strategy/datas.csv"
btc_historic_data = "./src/services/strategy/Binance_BTCGBP_d.csv"
stocksymbols = "TSLA"
startdate = date(2017,8,4)
end_date = date.today()

def retrieve_chained_header_item(df, first_key, second_key):
    return df[:, (first_key, second_key)]

def get_history(stocks=stocksymbols, start=startdate, end=end_date):
    # start=datetime.datetime(2018, 1, 1), end=datetime.datetime(2020, 12, 2)
    df: pd.DataFrame = pdr.get_data_yahoo(stocks, start=start, end=end) #['Close']
    df["Date"]= pd.to_datetime(df.index) # Redundant - values in correct format
    df.set_index('Date', inplace=True)
    df.to_csv('df_history.csv', sep=',', index=False, encoding='utf-8')
    return df

def get_pair_history(df_history: pd.DataFrame, pair: str):
    pair_history: pd.DataFrame = pd.DataFrame()
    for col_name in df_history.columns:
        if pair in col_name:
            pair_history[col_name[0]] = df_history[col_name]
    pair_history.to_csv('pair_history.csv', sep=',', index=False, encoding='utf-8')
    return pair_history

def relative_strength_index(df: pd.DataFrame, days):
    return ta.rsi(df['Close'], int(days))

def simple_moving_average(df: pd.DataFrame, days):
    return ta.sma(df['Close'], int(days))

def append_sma_to_df(df: pd.DataFrame):
    df.ta.sma(length=100, append=True)

def append_rsi_to_df(df: pd.DataFrame):
    df.ta.rsi(length=100, append=True)

def plot(df: pd.DataFrame, indicator: str):
    if indicator == "rsi":
        plt.plot(df.Date, df.RSI_100)
    elif indicator == "sma":
        plt.plot(df.Date, df.SMA_100)

def create_plot_graph(df: pd.DataFrame):
    plt.plot(df.Date, df.Close)
    append_rsi_to_df(df)
    append_sma_to_df(df)
    df.ta.indictators()
    plot(df, "rsi")
    plot(df, "sma")
    plt.show()

def show_chart():
    macd_obj = MACD(base, second_currency, period, fast, slow, signal)
    df = macd_obj.df
    hadf=ta.ha(
        open_=df.Open,
        high=df.High,
        low=df.Low,
        close=df.Close
    )
    fig = go.Figure(data=[go.Candlestick(
        x=df.Date,
        open=hadf.HA_open,
        high=hadf.HA_high,
        low=hadf.HA_low,
        close=hadf.HA_close,
        increasing_line_color="green",
        decreasing_line_color="red",
    )])
    fig.show()

def buy_sell(df: pd.DataFrame):
    signalBuy = []
    signalSell = []
    position = False 

    for index, row in df.iterrows():
        if row['SMA 30'] > row['SMA 100']:
            if position == False:
                signalBuy.append(row['Adj Close'])
                signalSell.append(np.nan)
                position = True
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        elif row['SMA 30'] < row['SMA 100']:
            if position == True:
                signalBuy.append(np.nan)
                signalSell.append(row['Adj Close'])
                position = False
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        else:
            signalBuy.append(np.nan)
            signalSell.append(np.nan)
    return pd.Series([signalBuy, signalSell])

stock_pairs = ['BTC-GBP', 'ETH-GBP', 'SOL-GBP']
signals = ['Buy_Signal_price', 'Sell_Signal_price']
days_collection = [30, 100]

df_history = get_history(stock_pairs)

for pair in stock_pairs:
    pair_history: pd.DataFrame = get_pair_history(df_history, pair)
    for days in days_collection:
        pair_history[f'SMA {days}'] = simple_moving_average(pair_history, days)
    pair_history[f'SMA {signals[0]}'], pair_history[f'SMA {signals[1]}'] = buy_sell(pair_history)

    print(pair_history)











# print("\n\n"+macd_obj.macd.to_json(orient='table'))
# print("\n\n"+macd_obj.macd.to_json(orient ='records'))
# print(f"\n\n")
# print(macd_obj.df)
# print(f"\n\n")
# print(macd_obj.macd)

# print(f"\n\n{macd_obj.macdh_config}")
# print(f"\n\n{macd_obj.macds_config}")

# macd_obj.create_fig()

# window = 12
# df[f"roc_{window}"] = momentum.ROCIndicator(close=df["Close"], window=window).roc()

# # Create your own Custom Strategy
# CustomStrategy = ta.Strategy(
#     name="Momo and Volatility",
#     description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
#     ta=[
#         {"kind": "sma", "length": 50},
#         {"kind": "sma", "length": 200},
#         {"kind": "bbands", "length": 20},
#         {"kind": "rsi"},
#         {"kind": "macd", "fast": 8, "slow": 21},
#         {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
#     ]
# )
# # To run your "Custom Strategy"
# df.ta.strategy(CustomStrategy)