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

def calculate_macd(df) -> pd.DataFrame:
    df_macd = ta.macd(df['Close'])
    return pd.concat([df, df_macd], axis=1).reindex(df.index)

def calculate_macd_trend(df) -> pd.DataFrame:
    macd_trend = ta.trend.MACD(df['Close'])
    df['MACD'] = macd_trend.macd()
    df['MACD_Signal'] = macd_trend.macd_signal()
    df['MACD_Diff'] = macd_trend.macd_diff()
    df.tail()
    return df

def macd_color(df):
    macd_color = []
    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['MACDh_12_26_9'] > df.iloc[ii-1]['MACDh_12_26_9']:
            macd_color.append(True)
        else:
            macd_color.append(False)
    return macd_color

def macd_strategy(df, risk):
    MACD_Buy=[]
    MACD_Sell=[]
    position=False

    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['MACD_12_26_9'] > row['MACDs_12_26_9']:
            MACD_Sell.append(np.nan)
            if position ==False:
                MACD_Buy.append(row['Adj Close'])
                position=True
            else:
                MACD_Buy.append(np.nan)
        elif row['MACD_12_26_9'] < row['MACDs_12_26_9']:
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(row['Adj Close'])
                position=False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and row['Adj Close'] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(row['Adj Close'])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and row['Adj Close'] < df.iloc[ii-1]['Adj Close'] * (1 - risk):
            MACD_Sell.append(row['Adj Close'])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    df['MACD_Buy_Signal_price'] = MACD_Buy
    df['MACD_Sell_Signal_price'] = MACD_Sell
    df['positive'] = macd_color(df)
    return df