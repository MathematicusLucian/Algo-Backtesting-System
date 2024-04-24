import pandas as pd
import yfinance as yf
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

data = pd.df = pd.read_csv("stock_data")
n_years = 1
period = n_years*365
data.reset_index(inplace = True)
df_train = data[['Date','Close']]
df_train = df_train.rename(columns = {"Date":"ds", "Close":'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)
print(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m,forecast)
# fig1 = m.plot(forecast)
fig1.savefig('prophet_plot.svg')
fig2 = m.plot_components(forecast)
fig1.savefig('prophet_components_plot.svg')