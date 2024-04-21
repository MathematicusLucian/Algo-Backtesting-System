from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
from src.services.strategy._old_macd import MACD
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
    ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.show()

def macd_charts(pair_key, data):
    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(pair_key, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot('Adj Close',data=data, label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)
    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index,'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),width=1,alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()
    plt.show()

def bollinger_chart(pair_key, data):
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(pair_key, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot(data['Adj Close'],label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['bb_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['bb_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)
    ax2.plot(data['BBM_20_2.0'], label='Middle', color='blue', alpha=0.35) #middle band
    ax2.plot(data['BBU_20_2.0'], label='Upper', color='green', alpha=0.35) #Upper band
    ax2.plot(data['BBL_20_2.0'], label='Lower', color='red', alpha=0.35) #lower band
    ax2.fill_between(data.index, data['BBL_20_2.0'], data['BBU_20_2.0'], alpha=0.1)
    ax2.legend(loc='upper left')
    ax2.grid()
    plt.show()