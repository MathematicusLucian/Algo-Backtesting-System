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