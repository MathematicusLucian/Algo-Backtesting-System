from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
from src.services.strategy._old_macd import MACD
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

def calculate_macd(df) -> pd.DataFrame:
    df_macd = ta.macd(df['Close'])
    return pd.concat([df, df_macd], axis=1).reindex(df.index)

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