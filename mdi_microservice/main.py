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
from src.charts import *

def retrieve_chained_header_item(df, first_key, second_key):
    return df[:, (first_key, second_key)]

def get_history(stocks, start=date(2017,8,4), end=date.today()):
    df: pd.DataFrame = pdr.get_data_yahoo(stocks, start=start, end=end) 
    df["Date"]= pd.to_datetime(df.index) 
    df.set_index('Date', inplace=True)
    # df.to_csv('df_history.csv', sep=',', index=False, encoding='utf-8')
    return df

def get_stock_pairs(df_history, stock_pairs_keys):
    stock_pairs_dict = dict()
    for pair in stock_pairs_keys:
        pair_history: pd.DataFrame = get_pair_history(df_history, pair)
        # pair_history.to_csv(f'pair-{pair}.csv', sep=',', index=False, encoding='utf-8')
        stock_pairs_dict[pair] = pair_history
    return stock_pairs_dict

def get_pair_history(df_history: pd.DataFrame, pair: str):
    pair_history: pd.DataFrame = pd.DataFrame()
    for col_name in df_history.columns:
        if pair in col_name:
            pair_history[col_name[0]] = df_history[col_name]
    pair_history = pair_history.dropna()
    pair_history.sort_values(by="Date", inplace=True)
    # pair_history.to_csv(f'pair_history_{pair}.csv', sep=',', index=False, encoding='utf-8')
    return pair_history

def relative_strength_index(df: pd.DataFrame, days):
    return ta.rsi(df['Close'], int(days))

def simple_moving_average(df: pd.DataFrame, days):
    return ta.sma(df['Close'], int(days))

def sma_strategy(stock_pairs_dict, signals, days_collection):
    index = 0
    for pair_name in stock_pairs_dict:
        index = index + 1
        data = stock_pairs_dict[pair_name]
        # stock_pairs_dict[pair_name].to_csv(f'sma-{index}.csv', sep=',', index=False, encoding='utf-8')
        for days in days_collection:
            data[f'SMA {days}'] = simple_moving_average(data, days)
        data[f'SMA {signals[0]}'], data[f'SMA {signals[1]}'] = sma_strategy_buy_sell(data)
        data.to_csv(f'strategy-output-{pair_name}.csv', sep=',', index=False, encoding='utf-8')

def sma_strategy_buy_sell(df: pd.DataFrame):
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

def macd(df):
    return ta.macd(df['Close'])

stock_pairs_keys = ['BTC-GBP', 'ETH-GBP', 'SOL-GBP']
signals = ['Buy_Signal_price', 'Sell_Signal_price']
days_collection = [30, 100]
base="USD"
second_currency="BTC"
period="1yr"
fast=12
slow=26
signal=9
start_date = date(2017,8,4)
end_date = date.today()

df_history = get_history(stock_pairs_keys, start_date, end_date)
stock_pairs_dict = get_stock_pairs(df_history, stock_pairs_keys)

sma_strategy(stock_pairs_dict, signals, days_collection)

pair_key = 'BTC-GBP'
pair = stock_pairs_dict[pair_key]
sma_chart(pair_key, pair, start_date, end_date)





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