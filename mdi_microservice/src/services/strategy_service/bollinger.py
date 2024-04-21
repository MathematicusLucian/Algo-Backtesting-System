from datetime import date
import numpy as np
import pandas as pd
# import talib
from ta import momentum
import pandas_ta as pta
from finta import TA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

def calculate_bollinger(df):
    bb = pta.bbands(df['Adj Close'], length=20,std=2)
    df = pd.concat([df, bb], axis=1).reindex(df.index)
    return df

# def bands(df):
#     upper, middle, lower = talib.BBANDS(df["Adj Close"], timeperiod=20)
#     bbands_talib = pd.DataFrame(index=df.index,
#                                 data={"bb_low": lower,
#                                     "bb_ma": middle,
#                                     "bb_high": upper})
#     return bbands_talib

def bollinger_strategy(df):
    bbBuy = []
    bbSell = []
    position = False
    # print(pta.bbands())

    for (index, row), ii in zip(df.iterrows(), range(len(df.index))):
        if row['Adj Close'] < row['BBL_20_2.0']:
            if position == False :
                bbBuy.append(row['Adj Close'])
                bbSell.append(np.nan)
                position = True
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        elif row['Adj Close'] > row['BBU_20_2.0']:
            if position == True:
                bbBuy.append(np.nan)
                bbSell.append(row['Adj Close'])
                position = False #To indicate that I actually went there
            else:
                bbBuy.append(np.nan)
                bbSell.append(np.nan)
        else :
            bbBuy.append(np.nan)
            bbSell.append(np.nan)

    df['bb_Buy_Signal_price'] = bbBuy
    df['bb_Sell_Signal_price'] = bbSell
    return df

def plot_bb(df):
    ta_bbands = pta.volatility.BollingerBands(close=df["Adj Close"], 
                                            window=20, 
                                            window_dev=2)
    ta_df = df.copy()
    ta_df["bb_ma"] = ta_bbands.bollinger_mavg()
    ta_df["bb_high"] = ta_bbands.bollinger_hband()
    ta_df["bb_low"] = ta_bbands.bollinger_lband()
    ta_df["bb_high_ind"] = ta_bbands.bollinger_hband_indicator()
    ta_df["bb_low_ind"] = ta_bbands.bollinger_lband_indicator()
    ta_df["bb_width"] = ta_bbands.bollinger_wband()
    ta_df["bb_pct"] = ta_bbands.bollinger_pband()
    ta_df[["bb_low", "bb_ma", "bb_high"]].plot(title="Bolinger Bands (ta)")
    return ta_df

# ta_all_indicators_df = ta.add_all_ta_features(df, open="Open", high="High", 
#                                               low="Low", close="Close", 
#                                               volume="Volume")
# ta_all_indicators_df.shape

# pta_df = pta.bbands(df["Adj Close"], length=20, talib=False)
# (
#     pta_df[["BBL_20_2.0", "BBM_20_2.0", "BBU_20_2.0"]]
#     .plot(title="Bolinger Bands (pandas_ta)")
# )

# finta_df = TA.BBANDS(df)
# (
#     finta_df[["BB_LOWER", "BB_MIDDLE", "BB_UPPER"]]
#     .plot(title="Bolinger Bands (FinTA)")
# )