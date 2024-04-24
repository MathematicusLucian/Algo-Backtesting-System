from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import matplotlib.pyplot as plt
import seaborn as sns
from src.services.strategy_service.ml.ml import ml
from src.services.strategy_service.system_strat import System
from src.services.strategy_service.rsi import RsiOscillator__Single, RsiOscillator__DailyWeekly
from src.services.strategy_service.sma import SmaCross

# bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
# stats = bt.run()
# stats = bt.optimize(n1=range(5, 30, 5),
#                     n2=range(10, 70, 5),
#                     maximize='Equity Final [$]',
#                     constraint=lambda param: param.n1 < param.n2)
# bt.plot(plot_volume=False, plot_pl=False)

# ml()

backtest = Backtest(GOOG, System, commission=.002)
backtest.run()
backtest.optimize(d_rsi=range(10, 35, 5),
                  w_rsi=range(10, 35, 5),
                  level=range(30, 80, 10))
backtest.plot()