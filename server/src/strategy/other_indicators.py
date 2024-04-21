from cmath import sqrt
from numpy import log, average
from .calculations import *
from .moving_averages import *
from .ad import *

class BollingerBands(Metric):
    def __init__(self, period=20, stdev=2.0, metric=None):
        if metric is None:
            self.metric       = Close()
            self.manageMetric = True
        else:
            self.metric       = metric
            self.manageMetric = False
        self.period = period
        self.stdev  = stdev
        self.sma    = SimpleMovingAverage(metric=self.metric, period=period)
        self.data   = list()

    def value(self):
        if not self.ready():
            return None
        arr = numpy.array(self.data)
        return numpy.std(arr) * self.stdev

    def upperBand(self):
        if not self.ready():
            return None
        return self.sma.value() + self.value()

    def lowerBand(self):
        if not self.ready():
            return None
        return self.sma.value() - self.value()

    def movingAverage(self):
        return self.sma.value()

    def percentB(self):
        if not self.ready():
            return None
        sma = self.sma.value()
        x = self.metric.value()
        bb = self.value()
        # range is 2x bb, so %b (0 at bottom) is (x-(sma-bb))/(2*bb)
        # note 2 here is unrelated to stdev multiplier but because
        # we have 2 bands, upper and lower
        v = (x - (sma-bb))
        if v == 0 or bb == 0:
            return 0
        return v/(2*bb)

    def ready(self):
        if len(self.data) >= self.period:
            return True
        return False

    def handle(self, periodData):
        if self.manageMetric:
            self.metric.handle(periodData)
        self.sma.handle(periodData)
        deviation = self.metric.value()
        self.data.append(deviation)
        if len(self.data) > self.period:
            self.data = self.data[(len(self.data) - self.period):]

    def recommendedPreload(self):
        return self.period*2

class BollingerBandsPercentB(Metric):
    def __init__(self, period=20, stdev=2.0, metric=None):
        self.bb = BollingerBands(period=period, stdev=stdev, metric=metric)

    def value(self):
        if self.bb.ready() == False:
            return None
        return self.bb.percentB()

    def ready(self):
        return self.bb.ready()

    def handle(self, periodData):
        self.bb.handle(periodData)

    def recommendedPreload(self):
        return self.bb.recommendedPreload()
    
class LogN(Metric):
    def __init__(self, metric):
        self.metric = metric
        self.val = None

    def ready(self):
        return self.metric.ready()

    def value(self):
        return self.val

    def handle(self, perioddata):
        if self.metric.ready():
            self.val = log(self.metric.value())

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class STDev(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.period=period
        self.data = list()

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def value(self):
        if self.ready():
            return numpy.std(self.data)
        return None

    def handle(self, perioddata):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data) > self.period:
                self.data = self.data[len(self.data)-self.period:]

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

# Not annualized, but dependent on data period 
class HistoricVolatility(Metric):
    def __init__(self, period=100, metric=None):
        if metric == None:
            self.metric = Close()
            self.manageMetric=True
        else:
            self.metric = metric
            self.manageMetric = False
        self.historicmetric = HistoricMetric(self.metric,1)
        self.div = Divide(self.metric, self.historicmetric)
        self.xi = LogN(self.div)
        self.xistd = STDev(self.xi,period)
        self.dataperiod = None

    def ready(self):
        return self.xistd.ready()

    def value(self):
        ret = self.xistd.value()
        days = float(self.dataperiod) / 86400.0
        # comp for weekends
        days = (7.0/5.0)*days
        if ret is None:
            return None
        return ret * (sqrt(252))

    def handle(self, perioddata):
        if self.dataperiod != None and self.dataperiod != perioddata.period:
            raise ValueError("HistoricVolatility was passed data with differing time intervals")
        self.dataperiod = perioddata.period
        if self.manageMetric:
            self.metric.handle(perioddata)
            self.historicmetric.handle(perioddata)
            self.div.handle(perioddata)
            self.xi.handle(perioddata)
            self.xistd.handle(perioddata)

    def recommendedPreload(self):
        return self.xistd.recommendedPreload()

class NumTaps(Metric):
    def __init__(self, metric, period, margin):
        self.metric=metric
        self.period=period
        self.margin=margin
        self.data = list()

    def value(self):
        if self.ready() == False:
            return None
        retval = 0
        high = max(self.data)
        for x in self.data:
            if (high - x) <= self.margin:
                retval = retval + 1
        return retval

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class NumTapsShort(Metric):
    def __init__(self, metric, period, margin):
        self.metric=metric
        self.period=period
        self.margin = margin
        self.data = list()

    def value(self):
        retval = 0
        if self.ready() == False:
            return None
        floor = min(self.data)
        for x in self.data:
            if (x-floor) <= self.margin:
                retval = retval + 1
        return retval

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class AverageVolume(MultiMetricMetric):
    def __init__(self, period=21):
        MultiMetricMetric.__init__(self)

        self.volume = Volume()
        self.avgVol = SimpleMovingAverage(self.volume, period)

        self._addMetric(self.volume)
        self._addMetric(self.avgVol)

    def value(self):
        return self.avgVol.value()

class AverageMetric(Metric):
    def __init__(self, *metrics):
        self.count=0
        self.metrics = metrics
        self.count = len(self.metrics)

    def ready(self):
        for metric in self.metrics:
            if not metric.ready():
                return False
        return True

    def value(self):
        values = list()
        for metric in self.metrics:
            if metric.ready() == False:
                return None
            values.append(metric.value())
        count = 0.0
        sum = 0.0
        for value in values:
            sum = sum + value
            count = count + 1.0
        if count == 0:
            return 0
        return sum/count
    
class ProxiedMetric(MultiMetricMetric):
    def __init__(self, metric):
        MultiMetricMetric.__init__(self)
        if metric == None:
            self.metric = Close()
            self._addMetric(self.metric)
        else:
            # do not manage it, just track it
            self.metric = metric

    def ready(self):
        return self.metric.ready()

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class PercentChange(ProxiedMetric):
    def __init__(self, metric=None):
        ProxiedMetric.__init__(self, metric)
        self.lastData = None
        self.val = None

    def ready(self):
        if self.val == None:
            return False
        return True

    def value(self):
        return self.val

    def handle(self, perioddata):
        ProxiedMetric.handle(self, perioddata)
        if self.metric.ready():
            if self.lastData != None:
                if self.lastData == 0:
                    self.val = 0
                else:
                    self.val = (self.metric.value() - self.lastData)/self.lastData
            self.lastData = self.metric.value()

    def recommendedPreload(self):
        return ProxiedMetric.recommendedPreload(self) + 1

class Highest(Metric):
    def __init__(self, metric, period):
        self.metric=metric
        self.period=period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return max(self.data)

    def ready(self):
        if len(self.data) == 0:
            return False
        if self.period == -1 and len(self.data)>0:
            return True
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if self.period > 0 and len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class Lowest(Metric):
    def __init__(self, metric, period):
        self.metric=metric
        self.period=period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return min(self.data)

    def ready(self):
        if len(self.data) == 0:
            return False
        if self.period == -1 and len(self.data)>0:
            return True
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if self.period > 0 and len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period


class TrueRange(Metric):
    def __init__(self):
        self.val = None
        self.lastClose = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.lastClose == None:
            self.lastClose = periodData.close
        self.val = max(periodData.high-periodData.low,self.lastClose-periodData.low,periodData.high-self.lastClose)
        self.lastClose = periodData.close

    def recommendedPreload(self):
        return 1


class AdjustedTrueRange(Metric):
    def __init__(self):
        self.val = None
        self.lastClose = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.lastClose == None:
            self.lastClose = periodData.adjustedClose
        self.val = max(periodData.adjustedHigh-periodData.adjustedLow,self.lastClose-periodData.adjustedLow,periodData.adjustedHigh-self.lastClose)
        self.lastClose = periodData.adjustedClose

    def recommendedPreload(self):
        return 1


class DMPos(Metric):
    def __init__(self):
        self.lasthigh = None
        self.lastlow = None
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if self.lasthigh != None and self.lastlow != None:
            up = max(periodData.high - self.lasthigh,0)
            down = max(self.lastlow - periodData.low, 0)
            if (up > down):
                self.val = up
            else:
                self.val = 0
        self.lasthigh = periodData.high
        self.lastlow = periodData.low

    def recommendedPreload(self):
        return 1

class DMNeg(Metric):
    def __init__(self):
        self.lasthigh = None
        self.lastlow = None
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if self.lasthigh != None and self.lastlow != None:
            up = max(periodData.high - self.lasthigh,0)
            down = max(self.lastlow - periodData.low, 0)
            if (up < down):
                self.val = down
            else:
                self.val = 0
        self.lasthigh = periodData.high
        self.lastlow = periodData.low

    def recommendedPreload(self):
        return 1