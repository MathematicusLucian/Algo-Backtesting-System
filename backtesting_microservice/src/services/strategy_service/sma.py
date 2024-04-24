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
# https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

        # if (self.sma1[-2] < self.sma2[-2] and
        #         self.sma1[-1] > self.sma2[-1]):
        #     self.position.close()
        #     self.buy()

        # elif (self.sma1[-2] > self.sma2[-2] and    # Ugh!
        #       self.sma1[-1] < self.sma2[-1]):
        #     self.position.close()
        #     self.sell()

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