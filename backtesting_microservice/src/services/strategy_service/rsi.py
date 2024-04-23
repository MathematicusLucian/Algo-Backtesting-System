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
from backtesting import Strategy
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG

class RsiOscillator__Single(Strategy):
    def init(self, *args, **kwargs): # upper_bound, lower_bound, rsi_window, tp=None, sl=None, size=None,
        # super(RsiOscillator__Single, self).__init__(self, upper_bound, lower_bound, rsi_window, tp=None, sl=None)
        # super().__init__(*args, **kwargs)
        super().init(self, *args, **kwargs)
    #     self.upper_bound = upper_bound
    #     self.lower_bound = lower_bound
    #     self.rsi_window = rsi_window
    #     self.sl = sl
    #     self.tp = tp
    #     self.size = size
    #     self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    def next(self):
        price = self.data.Close[-1]
    #     if crossover(self.rsi, self.upper_bound):
    #         self.position.close()
    #     elif crossover(self.lower_bound, self.rsi):
    #         if self.tp != None and self.sl !=None:
    #             self.buy(tp=self.tp*price, sl=self.sl*price)
    #         elif self.size != None:
    #             self.buy(size=0.1)
    #         else:
    #             self.buy()

class RsiOscillator__DailyWeekly(Strategy):
    def init(self, upper_bound, lower_bound, rsi_window):
        super(RsiOscillator__DailyWeekly, self).__init__(upper_bound, lower_bound, rsi_window, tp=None, sl=None)
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.rsi_window = rsi_window
        self.daily_rsi = self.I(ta.rsiI, pd.Series(self.data.Close), self.rsi_window)
        self.weekly_rsi = resample_apply(
            'W-FRI', ta.rsi, pd.Series(self.data.Close), self.rsi_window
        )

    def next(self):
        if (crossover(self.daily_rsi, self.upper_bound) and
                self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()
        elif (crossover(self.lower_bound, self.daily_rsi) and
                self.lower_bound > self.weekly_rsi[-1]):
            self.buy()

def relative_strength_index(df: pd.DataFrame, days):
    return ta.rsi(df['Close'], int(days))