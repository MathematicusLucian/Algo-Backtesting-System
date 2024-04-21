from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

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
        # data.to_csv(f'strategy-output-{pair_name}.csv', sep=',', index=False, encoding='utf-8')

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