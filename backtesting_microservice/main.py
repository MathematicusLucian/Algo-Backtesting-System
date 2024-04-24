from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import matplotlib.pyplot as plt
import seaborn as sns
from src.services.strategy_service.macd import MACDStrategy
from src.services.strategy_service.ml.ml import ml
from src.services.strategy_service.system_strat import System
from src.services.strategy_service.rsi import RsiOscillator__Single, RsiOscillator__DailyWeekly
from src.services.strategy_service.sma import Sma4Cross, SmaCross

#SciKit Machine Learning
# ml()

# System
# backtest = Backtest(GOOG, System, commission=.002)
# backtest.run()
# backtest.optimize(d_rsi=range(10, 35, 5),
#                   w_rsi=range(10, 35, 5),
#                   level=range(30, 80, 10))
# backtest.plot()

bt = Backtest(GOOG, MACDStrategy, cash=10000, commission=.002, exclusive_orders=True)
results = bt.run()
print(results)
bt.plot()