from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import matplotlib.pyplot as plt
import seaborn as sns
from src.services.strategy_service.ml.ml import ml
from src.services.strategy_service.system_strat import System
from src.services.strategy_service.rsi import RsiOscillator__Single, RsiOscillator__DailyWeekly
from src.services.strategy_service.sma import Sma4Cross, SmaCross

#SciKit Machine Learning
# ml()

# Trailing
bt = Backtest(GOOG, SmaCross, commission=.002)
bt.run()
bt.plot()

# bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
# stats = bt.run()
# stats = bt.optimize(n1=range(5, 30, 5),
#                     n2=range(10, 70, 5),
#                     maximize='Equity Final [$]',
#                     constraint=lambda param: param.n1 < param.n2)
# bt.plot(plot_volume=False, plot_pl=False)

# System
# backtest = Backtest(GOOG, System, commission=.002)
# backtest.run()
# backtest.optimize(d_rsi=range(10, 35, 5),
#                   w_rsi=range(10, 35, 5),
#                   level=range(30, 80, 10))
# backtest.plot()

# Heatmap
# backtest = Backtest(GOOG, Sma4Cross, commission=.002)
# stats, heatmap = backtest.optimize(
#     n1=range(10, 110, 10),
#     n2=range(20, 210, 20),
#     n_enter=range(15, 35, 5),
#     n_exit=range(10, 25, 5),
#     constraint=lambda p: p.n_exit < p.n_enter < p.n1 < p.n2,
#     maximize='Equity Final [$]',
#     max_tries=200,
#     random_state=0,
#     return_heatmap=True)
# heatmap.sort_values().iloc[-3:]
# hm = heatmap.groupby(['n1', 'n2']).mean().unstack()
# sns.heatmap(hm[::-1], cmap='viridis')
# plot_heatmaps(heatmap, agg='mean')
# stats_skopt, heatmap, optimize_result = backtest.optimize(
#     n1=[10, 100],      # Note: For method="skopt", we
#     n2=[20, 200],      # only need interval end-points
#     n_enter=[10, 40],
#     n_exit=[10, 30],
#     constraint=lambda p: p.n_exit < p.n_enter < p.n1 < p.n2,
#     maximize='Equity Final [$]',
#     method='skopt',
#     max_tries=200,
#     random_state=0,
#     return_heatmap=True,
#     return_optimization=True)
# heatmap.sort_values().iloc[-3:]
# from skopt.plots import plot_objective, plot_evaluations
# _ = plot_objective(optimize_result, n_points=10)
# _ = plot_evaluations(optimize_result, bins=10)