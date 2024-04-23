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

def calculate_sma__days(df: pd.DataFrame, days):
    return ta.sma(df['Close'], int(days))

def calculate_sma(data, days_collection):
    for days in days_collection:
        data[f'SMA {days}'] = calculate_sma__days(data, days)
    # stock_pairs_dict[pair_name].to_csv(f'sma-{index}.csv', sep=',', index=False, encoding='utf-8')
    # data.to_csv(f'strategy-output-{pair_name}.csv', sep=',', index=False, encoding='utf-8')
    return data

def sma_strategy(data, signals):
    data[f'SMA {signals[0]}'], data[f'SMA {signals[1]}'] = sma_strategy_buy_sell(data)
    return data

def sma_strategy_buy_sell(df: pd.DataFrame):
    signalBuy = []
    signalSell = []
    position = False 

    for index, row in df.iterrows():
        if (row['SMA 30'] > row['SMA 10']) and (row['SMA 10'] > row['SMA 50']) and (row['SMA 30'] > row['SMA 50']) and (row['SMA 200'] > row['SMA 10']) and (row['SMA 200'] > row['SMA 30']) and (row['SMA 200'] > row['SMA 50']):
            if position == False:
                signalBuy.append(row['Adj Close'])
                signalSell.append(np.nan)
                position = True
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        elif (row['SMA 30'] < row['SMA 10']) and (row['SMA 10'] < row['SMA 50']) and (row['SMA 30'] < row['SMA 50']) and (row['SMA 200'] < row['SMA 10']) and (row['SMA 200'] < row['SMA 30']) and (row['SMA 200'] < row['SMA 50']):
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