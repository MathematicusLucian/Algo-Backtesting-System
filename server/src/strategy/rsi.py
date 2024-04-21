from cmath import sqrt
from numpy import log, average
from .calculations import *
from .moving_averages import *

class RSI(Metric):
    def __init__(self, period=14, metric=None):
        if metric == None:
            self.metric = Close()
            self.manageMetric = True
        else:
            self.metric=metric
            self.manageMetric = False
        self.initgains = list()
        self.initlosses = list()
        self.averageGain=None
        self.averageLoss=None
        self.lastVal = None
        self.rsi = None
        self.period=period

    def value(self):
        return self.rsi

    def ready(self):
        if self.rsi != None:
            return True
        return False

    def handle(self, periodData):
        if self.manageMetric:
            self.metric.handle(periodData)
        if self.metric.ready():
            val = self.metric.value()
            if self.lastVal != None:
                delta = val - self.lastVal
                gain = max(0.0,delta)
                loss = max(0.0, -1.0*delta)
                if self.initgains != None:
                    self.initgains.append(gain)
                else:
                    self.averageGain = ((self.averageGain*(float(self.period-1))) + gain)/float(self.period)
                if self.initlosses != None:
                    self.initlosses.append(loss)
                else:
                    self.averageLoss = ((self.averageLoss*(float(self.period-1))) + loss)/float(self.period)
                if self.initgains != None and len(self.initgains) == self.period:
                    self.averageGain = sum(self.initgains)/float(self.period)
                    self.initgains = None
                if self.initlosses != None and len(self.initlosses) == self.period:
                    self.averageLoss = sum(self.initlosses)/float(self.period)
                    self.initlosses = None
                if self.averageGain != None and self.averageLoss != None:
                    if self.averageGain == 0 and self.averageLoss == 0:
                        self.rsi = 50
                    elif self.averageGain == 0:
                        self.rsi = 0
                    elif self.averageLoss == 0:
                        self.rsi = 100
                    else:
                        rs = self.averageGain/self.averageLoss
                        self.rsi = 100 - (100/(1+rs))
            self.lastVal = val

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)
