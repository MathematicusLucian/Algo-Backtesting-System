from datetime import date
import numpy as np
import pandas as pd
import pandas_ta as ta
from ta import momentum
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
plt.style.use('fivethirtyeight')
from src.charts import *
# from src.services.strategy._old_macd import MACD
from src.services.strategy.bollinger import *
from src.services.strategy.macd import *
from src.services.strategy.rsi import *
from src.services.strategy.sma import *
from src.services.history import *

stock_pairs_keys = ['BTC-GBP', 'ETH-GBP', 'SOL-GBP']
signals = ['Buy_Signal_price', 'Sell_Signal_price']
days_collection = [30, 100]
base="USD"
second_currency="BTC"
period="1yr"
fast=12
slow=26
signal=9
start_date = date(2017,8,4)
end_date = date.today()
df_history = get_history(stock_pairs_keys, start_date, end_date)
stock_pairs_dict = get_stock_pairs(df_history, stock_pairs_keys)
pair_key = 'BTC-GBP'
pair_data = stock_pairs_dict[pair_key]

# --- SMA ---
# sma_strategy(stock_pairs_dict, signals, days_collection)
# sma_chart(pair_key, pair_data, start_date, end_date)

# --- MACD ---
pair_data: pd.DataFrame = calculate_macd(pair_data)
df_macd_strategy_outcome = macd_strategy(pair_data, 0.025)
# macd_charts(pair_key, df_macd_strategy_outcome)

# --- Bollinger ---
pair_data = calculate_bollinger(df_macd_strategy_outcome)
df_bollinger_strategy_outcome = bollinger_strategy(pair_data)
bollinger_chart(pair_key, df_bollinger_strategy_outcome)