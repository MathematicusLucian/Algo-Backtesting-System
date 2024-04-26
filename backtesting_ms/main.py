from datetime import datetime
from altair import Stream
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import seaborn as sns
from src.strategies.sma import SmaCross
from src.services.strategy_service.trading_strategy_factory import TradingStrategy_ConcreteCreator

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
    trading_strategies = ["SmaCross"] #, "RsiOscillator"]
    for strats in trading_strategies:
        trading_strategy: type[Strategy] = trading_strategy_factory.get_trading_stategy(strats)
        bt = Backtest(GOOG, trading_strategy, cash=10_000, commission=.002)
        stats = bt.run()
        # # stats = bt.optimize(n1=range(5, 30, 5),
        # #                     n2=range(10, 70, 5),
        # #                     maximize='Equity Final [$]',
        # #                     constraint=lambda param: param.n1 < param.n2)
        bt.plot(plot_volume=False, plot_pl=False)