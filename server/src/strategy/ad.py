from cmath import sqrt
from numpy import log, average
from .calculations import *
from .moving_averages import *

class _ADXSmoother(Metric):
    def __init__(self,metric,period):
        self.metric = metric
        self.period = period
        self.val = None
        self.aggregator = list()

    def value(self):
        return self.val / self.period

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.aggregator != None:
            self.aggregator.append(self.metric.value())
            if len(self.aggregator) == self.period:
                self.val = sum(self.aggregator)
                self.aggregator = None
        if self.val != None:
            self.val = self.val * (1.0-(1.0/self.period)) + self.metric.value()

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class ADR(Metric):
    def __init__(self,period):
        self.high = High()
        self.low = Low()
        self.dr = Subtract(self.high, self.low)
        self.drav = SimpleMovingAverage(self.dr,period)

    def value(self):
        if self.drav.ready():
            return self.drav.value()
        return None

    def ready(self):
        return self.drav.ready()

    def handle(self, periodData):
        self.high.handle(periodData)
        self.low.handle(periodData)
        self.dr.handle(periodData)
        self.drav.handle(periodData)

    def recommendedPreload(self):
        return self.drav.recommendedPreload()

class ATR(Metric):
    def __init__(self,period):
        self.tr = TrueRange()
        self.trav = _ADXSmoother(self.tr,period)

    def value(self):
        if self.trav.ready():
            return self.trav.value()
        return None

    def ready(self):
        return self.trav.ready()

    def handle(self, periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)

    def recommendedPreload(self):
        return self.trav.recommendedPreload()

class AdjustedATR(Metric):
    def __init__(self,period):
        self.tr = AdjustedTrueRange()
        self.trav = _ADXSmoother(self.tr,period)

    def value(self):
        if self.trav.ready():
            return self.trav.value()
        return None

    def ready(self):
        return self.trav.ready()

    def handle(self, periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)

    def recommendedPreload(self):
        return self.trav.recommendedPreload()

class HistoricMetric(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.period = period
        self.data = list()

    def value(self):
        if self.ready():
            return self.data[self.period]
        return None

    def ready(self):
        if len(self.data)>self.period:
            return True
        return False

    def handle(self,periodData):
        if self.metric.ready():
            self.data.insert(0, self.metric.value())
        if len(self.data) > (self.period+1):
            self.data = self.data[0:self.period+1]

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class _ADXAverager(Metric):
    def __init__(self,metric,period):
        self.aggregator = list()
        self.val = None
        self.period = period
        self.metric = metric

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.aggregator != None:
            self.aggregator.append(self.metric.value())
            if len(self.aggregator) == self.period:
                self.val = sum(self.aggregator)/self.period
                self.aggregator = None
        if self.val != None:
            self.val = self.val * (1.0-(1.0/self.period)) + self.metric.value() * (1.0/self.period)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class ADX(Metric):
    def __init__(self,period):
        self.period = period
        self.tr = TrueRange()
        self.trav = _ADXSmoother(self.tr, period)
        self.dmpos = DMPos()
        self.dmneg = DMNeg()
        self.dmposav = _ADXSmoother(self.dmpos, period)
        self.dmnegav = _ADXSmoother(self.dmneg, period)
        self.dipos = Divide(self.dmposav, self.trav)
        self.dineg = Divide(self.dmnegav, self.trav)
        self.didiff = Subtract(self.dipos, self.dineg)
        self.didiffabs = Abs(self.didiff)
        self.disum = Add(self.dipos, self.dineg)
        self.dx = Divide(self.didiffabs, self.disum)
        self.adx = _ADXAverager(self.dx, period)

    def value(self):
        if self.adx.ready():
            return self.adx.value() * 100.0
        else:
            return 0.0

    def ready(self):
        return self.adx.ready()

    def handle(self,periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)
        self.dmpos.handle(periodData)
        self.dmneg.handle(periodData)
        self.dmposav.handle(periodData)
        self.dmnegav.handle(periodData)
        self.dipos.handle(periodData)
        self.dineg.handle(periodData)
        self.didiff.handle(periodData)
        self.didiffabs.handle(periodData)
        self.disum.handle(periodData)
        self.dx.handle(periodData)
        self.adx.handle(periodData)

    def diPos(self):
        if self.ready():
            return self.dipos.value()
        return None

    def diNeg(self):
        if self.ready():
            return self.dineg.value()

    def recommendedPreload(self):
        return self.adx.recommendedPreload()