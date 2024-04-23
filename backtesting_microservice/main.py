from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import matplotlib.pyplot as plt
import seaborn as sns
from src.services.strategy_service.rsi import RsiOscillator__Single, RsiOscillator__DailyWeekly
from src.services.strategy_service.sma import SmaCross

def optim_func(series):
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']
    
def sma(asset: str, cash: int, commission: int, exclusive_orders: bool = False) -> Backtest:
    strat = SmaCross(
        n1=10,
        n2=20
    )
    return Backtest(asset, strat, cash=cash, commission=commission, exclusive_orders=exclusive_orders)

def rsi(asset: str, cash: int, commission: int) -> Backtest:
    strat = RsiOscillator__Single(
        upper_bound=70, 
        lower_bound=30, 
        rsi_window=14, 
        tp=1.15, 
        sl=0.95,
    )
    return Backtest(asset, strat, cash=cash, commission=commission)

# bt: Backtest = sma(GOOG, 10000, .002, True)
bt: Backtest = rsi(GOOG, 10_000, .002)
# output = bt.run()
# print(f"\n\n{output["_strategy"]}\n\n")
# print(output['_trades'].to_string())
bt.plot()

# output, heatmap = bt.optimize(
#         upper_bound = range(50,85,5),
#         lower_bound = range(15,45,5),
#         rsi_window = range(10,30,2),
#         # maximize='Equity Final [$]'
#         maximize=optim_func,
#         return_heatmap=True)
# hm = heatmap.groupby(["upper_bound","lower_bound"]).mean().unstack()
# sns.heatmap(hm, cmap="plasma")
# plt.show()