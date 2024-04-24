from datetime import datetime
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import seaborn as sns
from src.services.strategy_service.macd import MACDStrategy
from src.services.strategy_service.ml.ml import ml
from src.services.strategy_service.system_strat import System
from src.services.strategy_service.rsi import RsiOscillator__Single, RsiOscillator__DailyWeekly
from src.services.strategy_service.sma import Sma4Cross, SmaCross

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

start = datetime(2022,1,1)
end = datetime(2024,1,1)
data = pdr.DataReader("TSLA","yahoo")
data.to_csv("data/stock_data.csv")

#SciKit Machine Learning
# ml()

# System
# backtest = Backtest(GOOG, System, commission=.002)
# backtest.run()
# backtest.optimize(d_rsi=range(10, 35, 5),
#                   w_rsi=range(10, 35, 5),
#                   level=range(30, 80, 10))
# backtest.plot()

# bt = Backtest(GOOG, MACDStrategy, cash=10000, commission=.002, exclusive_orders=True)
# results = bt.run()
# print(results)
# bt.plot()