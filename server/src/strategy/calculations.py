from cmath import sqrt
from numpy import log, average

class Metric:
    def __init__(self):
        pass

    def value(self):
        return 0

    def ready(self):
        return False

    def handle(self, perioddata):
        pass

    def recommendedPreload(self):
        return 0

class Add(Metric):
    def __init__(self, metric1, metric2):
        self.metric1=metric1
        self.metric2=metric2

    def value(self):
        return self.metric1.value() + self.metric2.value()

    def ready(self):
        if self.metric1.ready() and self.metric2.ready():
            return True
        return False

    def handle(self, periodData):
        pass

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Subtract(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        if self.ready():
            return self.metric1.value() - self.metric2.value()
        return None

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Multiply(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        a = self.metric1.value()
        b = self.metric2.value()
        return a*b

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Divide(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        a = self.metric1.value()
        b = self.metric2.value()
        if a == 0:
            return 0
        if b == 0:
            return 0
        return a/b

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())


class Abs(Metric):
    def __init__(self, metric):
        self.metric = metric

    def value(self):
        if self.metric.ready():
            return abs(self.metric.value())
        return 0

    def ready(self):
        return self.metric.ready()

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class Max(Metric):
    def __init__(self, metrica, metricb):
        self.metrica = metrica
        self.metricb = metricb

    def value(self):
        if self.ready() == False:
            return None
        return max(self.metrica.value(), self.metricb.value())

    def ready(self):
        return self.metrica.ready() and self.metricb.ready()

    def recommendedPreload(self):
        return max(self.metrica.recommendedPreload(), self.metricb.recommendedPreload())

class Value(Metric):
    def __init__(self, value):
        self.val = value

    def value(self):
        return self.val

    def ready(self):
        return True

class Open(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, perioddata):
        self.val = perioddata.open

class Close(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.close

class AdjustedClose(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedClose != None:
            self.val = periodData.adjustedClose

class AdjustedOpen(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedOpen != None:
            self.val = periodData.adjustedOpen

class AdjustedHigh(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedHigh != None:
            self.val = periodData.adjustedHigh

class AdjustedLow(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedLow != None:
            self.val = periodData.adjustedLow

class High(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.high

class Low(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.low

class MultiMetricMetric(Metric):
    def __init__(self):
        self.metrics = list()

    def _addMetric(self, metric):
        self.metrics.append(metric)

    def _addMetrics(self, *metrics):
        for metric in metrics:
            self._addMetric(metric)

    def ready(self):
        for metric in self.metrics:
            if metric.ready() == False:
                return False
        return True

    def handle(self, perioddata):
        for metric in self.metrics:
            metric.handle(perioddata)

    def recommendedPreload(self):
        retval = 0
        for metric in self.metrics:
            if metric.recommendedPreload() > retval:
                retval = metric.recommendedPreload()
        return retval

class Volume(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, perioddata):
        self.val = perioddata.volume