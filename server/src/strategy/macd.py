import yfinance as yf
import numpy as np
from pandas import DataFrame
import pandas_ta as ta
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class MACD:
    def __init__(self, pair, period, fast=12, slow=26, signal=9):
        self.colour_negative = '#006A4E'
        self.colour_positive = '#8e1600'
        self.df:DataFrame=self.get_currency_data(pair, period)
        self.macd:DataFrame
        self.fast=fast
        self.slow=slow
        self.signal=signal
        self.macdh_config = str(f'macdh_{fast}_{slow}_{signal}')
        self.macds_config = str(f'macds_{fast}_{slow}_{signal}')
        self.calculate_MACD()

    def macd_data(self):
        macd_data=dict()
        macd_data["macd"]=self.macd
        macd_data["price_line"]=self.price_line()
        macd_data["fast_signal"]=self.fast_signal()
        macd_data["slow_signal"]=self.slow_signal()
        macd_data["histogram"]=self.get_histogram()
        return macd_data

    def get_currency_data(self, pair, period):
        return yf.Ticker(pair).history(period=period)[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]

    def calculate_MACD(self):
        self.macd = self.df.ta.macd(close='close', fast=12, slow=26, append=True)
        self.macd.columns = [x.lower() for x in self.macd.columns]
    
    def get_historgram_colorized(self, df: DataFrame):
        return np.where(df[self.macdh_config] < 0, '#000', self.colour_positive)
    
    def get_layout():
        return go.Layout(
            plot_bgcolor='#efefef',
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
    
    def get_scatter(self, name, color, y, width, legendgroup):
        return go.Scatter(
                x=self.macd.index,
                y=y,
                line=dict(color=color, width=width),
                legendgroup=legendgroup,
                name=name
            )
    
    def get_candlesticks(self):
        return go.Candlestick(
                x=self.macd.index,
                open=self.macd['open'],
                high=self.macd['high'],
                low=self.macd['low'],
                close=self.macd['close'],
                increasing_line_color=self.colour_positive,
                decreasing_line_color='black',
                showlegend=False
            )
    
    def price_line(self):
        return self.get_scatter('open', self.colour_positive, self.macd['open'], 1, '1')
    
    def fast_signal(self):
        return self.get_scatter('Fast Signal (k)', self.colour_positive, self.macd[self.macds_config], 2, '2')
    
    def slow_signal(self):
        return self.get_scatter('Slow signal (d)', '#000000', self.macd[self.macds_config], 2, '2')
    
    def get_histogram(self):
        return go.Bar(
                x=self.macd.index,
                y=self.macd[self.macdh_config],
                name='histogram',
                marker_color=self.get_historgram_colorized(self.macd),
            )

    def create_fig(self):
        fig = make_subplots(rows=2, cols=1)
        fig.append_trace(self.price_line(), row=1, col=1)
        fig.append_trace(self.get_candlesticks(), row=1, col=1)
        fig.append_trace(self.fast_signal(), row=2, col=1)
        fig.append_trace(self.slow_signal(), row=2, col=1)
        fig.append_trace(self.get_histogram(), row=2, col=1)
        fig.update_layout(self.get_layout())
        fig.show()