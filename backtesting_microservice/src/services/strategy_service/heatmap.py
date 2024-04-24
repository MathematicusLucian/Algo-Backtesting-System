from backtesting import Backtest
# https://kernc.github.io/backtesting.py/doc/examples/Parameter%20Heatmap%20&%20Optimization.html
import matplotlib.pyplot as plt
import seaborn as sns

def optim_func(series):
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']

def create_heatmap(bt: Backtest):
    output, heatmap = bt.optimize(
        upper_bound = range(50,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,30,2),
        # maximize='Equity Final [$]'
        maximize=optim_func,
        return_heatmap=True
    )
    hm = heatmap.groupby(["upper_bound","lower_bound"]).mean().unstack()
    sns.heatmap(hm, cmap="plasma")
    plt.show()