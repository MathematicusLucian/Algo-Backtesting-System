from cmath import sqrt
from numpy import log, average
import config
import yfinance
import pandas as pd
import datetime
from requests_html import HTMLSession
from .calculations import *
from .other_indicators import *
from .ad import *

class config:
    LOOK_BACK_DAYS = 200
    SMALLER_LOOK_BACK_DAYS = 50
    MAXIMUM_CRYPTOS_TO_CONSIDER = 200 # Over 250 is not recommended

# -------------------------
# - SIMPLE MOVING AVERAGE -
# -------------------------

class SimpleMovingAverage(Metric):
    def __init__(self, metric=None, period=20):
        if metric == None:
            self.metric = AdjustedClose()
            self.manageMetric=True
        else:
            self.metric = metric
            self.manageMetric=False
        self.period = period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return numpy.average(self.data)

    def ready(self):
        if len(self.data) >= self.period:
            return True
        return False

    def handle(self, periodData):
        if self.manageMetric ==  True:
            self.metric.handle(periodData)
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data) > self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

# -------------------------
# -- EXPO MOVING AVERAGE --
# -------------------------

class ExponentialMovingAverage(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.multiplier = (2.0/(period+1))
        self.sma = SimpleMovingAverage(metric, period)
        self.period = period
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.sma != None:
            self.sma.handle(periodData)
            if self.sma.ready():
                self.val = self.sma.value()
                self.sma = None
        if self.val != None:
            newdat = self.metric.value()
            self.val = (newdat - self.val)*self.multiplier + self.val

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

# -------------------------
# ------ MOMENTUM ---------
# -------------------------

class Momentum(MultiMetricMetric):
    def __init__(self, period=14):
        MultiMetricMetric.__init__(self)
        self.close = AdjustedClose()
        self.old_close = HistoricMetric(metric=self.close, period=period)
        self._addMetrics(self.close, self.old_close)

    def value(self):
        delta = self.close.value() - self.old_close.value()
        if delta == 0:
            return 0
        if self.old_close.value() == 0:
            return 0
        return delta/self.old_close.value()

# -------------------------
# --------- MACD ----------
# -------------------------

class MACD(ProxiedMetric):
    def __init__(self, metric, fastma=12, slowma=26, signalma=9):
        ProxiedMetric.__init__(self, metric)
        self.fastma = ExponentialMovingAverage(metric, fastma)
        self.slowma = ExponentialMovingAverage(metric, slowma)
        self.macdline = Subtract(self.fastma,self.slowma)
        self.signalma = ExponentialMovingAverage(self.macdline, signalma)
        self.macdhist = Subtract(self.macdline, self.signalma)

        self._addMetric(self.fastma)
        self._addMetric(self.slowma)
        self._addMetric(self.macdline)
        self._addMetric(self.signalma)
        self._addMetric(self.macdhist)

    def value(self):
        return self.macdhist.value()

def date_string_to_datetime(date_string):
	return datetime.datetime.strptime(date_string, "%Y-%m-%d")

def get_next_day_string(current_day_string):
	current_day_datetime = date_string_to_datetime(current_day_string)
	next_day_datetime = current_day_datetime + datetime.timedelta(days=1)
	next_day_string = next_day_datetime.strftime("%Y-%m-%d")
	return next_day_string

def date_range(start_datetime, end_datetime):
    for i in range(int((end_datetime - start_datetime).days) + 1):
        yield start_datetime + datetime.timedelta(i)

def get_data_for_pair_name(pair_name, start_time, end_time):
	df = yfinance.download(pair_name, start=get_next_day_string(start_time), end=get_next_day_string(end_time), interval="1d", auto_adjust=True, prepost=True, threads=True)
	df = df.reset_index()
	df = df.dropna()
	df = df.loc[~df.apply(lambda row: (row == 0).any(), axis=1)]
	if df.shape[0] == 0:
		return df
	df["Close to Open Percent"] = df.apply(lambda row: 100 * (row.Close - row.Open) / row.Open, axis=1)
	df["High to Open Percent"] = df.apply(lambda row: 100 * (row.High - row.Open) / row.Open, axis=1)
	df["Low to Open Percent"] = df.apply(lambda row: 100 * (row.Low - row.Open) / row.Open, axis=1)
	df["High to Low Percent"] = df.apply(lambda row: 100 * (row.High - row.Low) / row.Low, axis=1)
	df = df.dropna()
	return df

def is_crypto_undervalued(df):
	moving_average = df.loc[:, "Close"].mean()
	last_close = df["Close"].iloc[-1]
	return last_close < moving_average, round(-100 * (moving_average - last_close) / last_close , 2)

def get_total_start_and_end_time(moving_average_size):
	start_time = datetime.datetime.utcnow() + datetime.timedelta(days=-moving_average_size)
	end_time = datetime.datetime.utcnow() + datetime.timedelta(days=-1)
	return start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")

def get_total_crypto_pair_names_list(maximum_cryptos_to_consider):
	html_session = HTMLSession()
	yfinance_response = html_session.get(f"https://finance.yahoo.com/crypto?offset=0&count={maximum_cryptos_to_consider}")
	df = pd.read_html(yfinance_response.html.raw_html)               
	df = df[0].copy()
	total_crypto_pair_names_list = df.Symbol.tolist()
	return total_crypto_pair_names_list

def detect_golden_cross_or_death_cross(df, smaller_moving_average_size):
	if  df["Close"][-smaller_moving_average_size:].mean() >= df["Close"].mean():
		return "GOLDEN CROSS"
	else:
		return "DEATH CROSS"

def get_cryptos_list_with_info(pair_name_names_list, start_time, end_time):
	undervalued_cryptos_list = []
	cryptos_list_with_stats = []
	for pair_name_name in pair_name_names_list:
		df = get_data_for_pair_name(pair_name_name, start_time, end_time)
		if df.shape[0] == 0:
			continue
		last_day_price_change_percent = round(100 * (df["Close"].iloc[-1] - df["Open"].iloc[-1]) / df["Open"].iloc[-1], 2)
		average_daily_close_to_open_percent = round(df["Close to Open Percent"].mean(), 2)
		average_daily_high_to_open_percent = round(df["High to Open Percent"].mean(), 2)
		average_daily_low_to_open_percent = round(df["Low to Open Percent"].mean(), 2)
		average_daily_high_to_low_percent = round(df["High to Low Percent"].mean(), 2)
		golden_cross_or_death_cross = detect_golden_cross_or_death_cross(df, config.SMALLER_LOOK_BACK_DAYS)
		cryptos_list_with_stats.append((pair_name_name[:-4],
			last_day_price_change_percent,
			average_daily_close_to_open_percent,
			average_daily_high_to_open_percent,
			average_daily_low_to_open_percent,
			average_daily_high_to_low_percent,
			golden_cross_or_death_cross))

		is_under, diff_percentage = is_crypto_undervalued(df)
		if is_under:
			undervalued_cryptos_list.append((pair_name_name[:-4], diff_percentage))
	cryptos_list_with_stats.sort(key=lambda tup: tup[1])
	return undervalued_cryptos_list, cryptos_list_with_stats

def run(moving_average_size, maximum_cryptos_to_consider):
	start_time, end_time = get_total_start_and_end_time(moving_average_size)
	crypto_pair_names_list = get_total_crypto_pair_names_list(maximum_cryptos_to_consider)
	cryptos_list_with_info = get_cryptos_list_with_info(crypto_pair_names_list, start_time, end_time)
	return cryptos_list_with_info

def determine_macd_crypto():
	data = {}
	undervalued_cryptos_list, pumped_or_dumped_cryptos_list = run(config.LOOK_BACK_DAYS, config.MAXIMUM_CRYPTOS_TO_CONSIDER)
	undervalued_cryptos_list.sort(key = lambda x: x[1])
	data["undervalued_cryptos_list"] = undervalued_cryptos_list
	data["pumped_or_dumped"] = {}
	for crypto_name, \
		last_day_price_change_percent, \
		average_daily_close_to_open_percent, \
		average_daily_high_to_open_percent, \
		average_daily_low_to_open_percent, \
		average_daily_high_to_low_percent, \
		golden_cross_or_death_cross in pumped_or_dumped_cryptos_list:
			data["pumped_or_dumped"][crypto_name] = [
				{"Last day price change percent": str(last_day_price_change_percent) + "%"},
                {"Average daily close to open percent": str(average_daily_close_to_open_percent) + "%"},
                {"Average daily high to open change percent": str(average_daily_high_to_open_percent) + "%"},
                {"Average daily low to open change percent": str(average_daily_low_to_open_percent) + "%"},
                {"Average daily high to low change percent": str(average_daily_high_to_low_percent) + "%"},
                {"Cross": golden_cross_or_death_cross}
			]
	data["based_on_past"] = f"{str(config.LOOK_BACK_DAYS)} days"
	data["cross_dectection"] = {f"MA{str(config.LOOK_BACK_DAYS)}": f"{str(config.SMALLER_LOOK_BACK_DAYS)}"}
	return data