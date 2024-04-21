from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
from src.services.strategy.macd import MACD
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
plt.style.use('fivethirtyeight')

def plot(df: pd.DataFrame, indicator: str):
    if indicator == "rsi":
        plt.plot(df.Date, df.RSI_100)
    elif indicator == "sma":
        plt.plot(df.Date, df.SMA_100)

def append_sma_to_df(df: pd.DataFrame):
    df.ta.sma(length=100, append=True)

def append_rsi_to_df(df: pd.DataFrame):
    df.ta.rsi(length=100, append=True)
    
def create_plot_graph(df: pd.DataFrame):
    plt.plot(df.Date, df.Close)
    append_rsi_to_df(df)
    append_sma_to_df(df)
    df.ta.indictators()
    plot(df, "rsi")
    plot(df, "sma")
    plt.show()

def show_chart(base, second_currency, period, fast, slow, signal):
    macd_obj = MACD(base, second_currency, period, fast, slow, signal)
    df = macd_obj.df
    hadf=ta.ha(
        open_=df.Open,
        high=df.High,
        low=df.Low,
        close=df.Close
    )
    fig = go.Figure(data=[go.Candlestick(
        x=df.Date,
        open=hadf.HA_open,
        high=hadf.HA_high,
        low=hadf.HA_low,
        close=hadf.HA_close,
        increasing_line_color="green",
        decreasing_line_color="red",
    )])
    fig.show()

def sma_chart(pair_key, data, start_date, end_date):
    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(data['Adj Close'], label = pair_key ,linewidth=0.5, color='blue', alpha = 0.9)
    ax.plot(data['SMA 30'], label = 'SMA30', alpha = 0.85)
    ax.plot(data['SMA 100'], label = 'SMA100' , alpha = 0.85)
    ax.scatter(data.index, data['SMA Buy_Signal_price'], label='Buy', marker='^', color='green', alpha=1 )
    ax.scatter(data.index, data['SMA Sell_Signal_price'], label='Sell', marker='v', color='red', alpha=1 )
    ax.set_title(pair_key + " Price History with buy and sell signals",fontsize=10, backgroundcolor='blue', color='white')
    ax.set_xlabel(f'{start_date} - {end_date}' ,fontsize=18)
    ax.set_ylabel('Close Price INR (₨)' , fontsize=18)
    legend = ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.show()