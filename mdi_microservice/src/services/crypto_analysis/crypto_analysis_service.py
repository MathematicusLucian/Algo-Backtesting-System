import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from src.utils.utils import get_root_dir

def fetch_currency_archive_data(currency):
    return pd.read_csv(f"{get_root_dir()}/backtesting_data/crypto_archive/{currency}.csv")

def create_plotly(df):
    fig = go.Figure(data=[go.Candlestick(x=df.date,
                open=df.open,
                high=df.high,
                low=df.low,
                close=df.close)])
    fig.show()

def get_min_date(df):
 return df.date.min()

def get_max_date(df):
 return df.date.max()

def get_range_for_number_of_days(df, days):
   return df.tail(days)

def get_range_between_dates(df, date_from, date_to):
   return df.loc[date_from:date_to]

def get_historic_data(currency, date_from, date_to):
    df = fetch_currency_archive_data(currency)
    return get_range_between_dates(df, date_from, date_to)