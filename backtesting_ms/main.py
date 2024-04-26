from datetime import datetime, date
# from altair import Stream
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
# from backtesting.lib import crossover, plot_heatmaps, resample_apply
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
# import matplotlib.pyplot as plt
# import seaborn as sns
from src.services.strategy_service import TradingStrategy_ConcreteCreator

trading_strategies = [
    "AverageDirectionalMovement",
    "BBandRSI",
    # "BBandRSI_WithStopLoss",
    # "BBandRSI_WithShortPosition",
    "BBsigma",
    # "BBsigma_WithShortPosition",
    "DonchianBreakout",
    # "DonchianBreakout_WithShortPosition",
    # "DonchianBreakout_WithATRStopLoss",
    # "DonchianBreakout_WithPercentageStopLoss",
    "EMA_Cross",
    # "EMA_Cross2",
    # "Ema_Cross__WithShortPosition",
    # "EntryRSIandExitSMA_WithShortPosition",
    # "EntryRSI50andExitBB",
    # "EntryRSI50andExitBB_WithShortPosition",
    # "EntryRSI50andExitBBWithATRStopLoss",
    # "GridStrat",
    # "Macd_25",
    # "Macd_25_2"
    # "MACDCross_WithShortPosition",
    # "MACDCross",
    # "MACDStrategy",
    # "MACDandBBD",
    # "MACDandBBD_WithShortPosition",
    # "MACDandRSI",
    # "MACDandRSI_WithShortPosition",
    "MeanReversion",
    "MeanReversionBollinger",
    "Momentum",
    "Momentum__Volatility",
    "MovingAverageCrossover",
    # "RsiOscillator",
    "RsiOscillator__Simple",
    "RsiOscillator__Simple_Close",
    # "RsiOscillator__Single",
    # "RsiOscillator__DailyWeekly",
    "RsiOscillator__LS_Close",
    "SmaCross", 
    "SmaCross__Trailing",
    "Sma4Cross",
    "SMAandRSI",
    "SMAandRSI_WithShortPosition",
    "Stochastic_OverboughtOversold",
    "StopLoss_ATR",
    # "StopLossFix",
    # "StopLoss_Percentage"
    # "StopLoss_Trailing",
    # "System",
    # "Turtle",
    # "Volatility_Breakout"
]

def optim_func(series):
    if series["Expectancy [%]"] < 0:
        return -1
    if series["Max. Drawdown [%]"] > 20:
        return -1
    if series["Profit Factor"] < 1:
        return -1
    if series["Sharpe Ratio"] < 1.5:
        return -1
    if series["SQN"] < 2.5:
        return -1
    if series["# Trades"] < 7:
        return -1
    if series["Win Rate [%]"] < 40:
        return -1
    if series["Worst Trade [%]"] < -20:
        return -1
    return series["Equity Final [$]"]

# ml() #SciKit Machine Learning

if __name__ == "__main__":
    trading_strategy_factory = TradingStrategy_ConcreteCreator()
    for strat in trading_strategies:
        trading_strategy: type[Strategy] = trading_strategy_factory.get_trading_stategy(strat)
        asset="BTC-GBP"
        start=date(2014,1,1) 
        end=date.today()
        bitcoin_df: pd.DataFrame = pdr.get_data_yahoo(asset, start=start, end=end) 
        bitcoin_df["Date"]= pd.to_datetime(bitcoin_df.index) 
        bt = Backtest(bitcoin_df, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run() # kwargs: set parameters
        # stats = bt.optimize(n1=range(5, 30, 5),
        #                     n2=range(10, 70, 5),
        #                     maximize="Win Rate [%]", #"Equity Final [$]", #"Profit Factor"
        #                     constraint=lambda param: param.n1 < param.n2)
        bt.plot(plot_volume=False, plot_pl=False)