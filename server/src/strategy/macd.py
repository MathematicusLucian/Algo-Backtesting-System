import yfinance as yf
# import matplotlib.pyplot as plt
import numpy as np
import pandas_ta as ta
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = yf.Ticker('BTC-USD').history(period='1y')[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]

df.ta.macd(close='close', fast=12, slow=26, append=True)
df.columns = [x.lower() for x in df.columns]

fig = make_subplots(rows=2, cols=1)

fig.append_trace( #price line
    go.Scatter(
        x=df.index,
        y=df['open'],
        line=dict(color='#ff9900', width=1),
        name='open',
        # showlegend=False,
        legendgroup='1',
    ), row=1, col=1
)

fig.append_trace( # candlestick chart for pricing
    go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#ff9900',
        decreasing_line_color='black',
        showlegend=False
    ), row=1, col=1
)
# Fast Signal (%k)
fig.append_trace(
    go.Scatter(
        x=df.index,
        y=df['macd_12_26_9'],
        line=dict(color='#ff9900', width=2),
        name='macd',
        # showlegend=False,
        legendgroup='2',
    ), row=2, col=1
)

fig.append_trace( # slow signal (%d)
    go.Scatter(
        x=df.index,
        y=df['macds_12_26_9'],
        line=dict(color='#000000', width=2),
        # showlegend=False,
        legendgroup='2',
        name='signal'
    ), row=2, col=1
)

historgram_colorized = np.where(df['macdh_12_26_9'] < 0, '#000', '#ff9900')

fig.append_trace( # plot the histogram
    go.Bar(
        x=df.index,
        y=df['macdh_12_26_9'],
        name='histogram',
        marker_color=historgram_colorized,
    ), row=2, col=1
)

layout = go.Layout(
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

fig.update_layout(layout)
fig.show()