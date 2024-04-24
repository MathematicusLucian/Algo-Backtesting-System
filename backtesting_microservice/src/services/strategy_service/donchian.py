from backtesting import Strategy
import pandas as pd
import talib as ta
import numpy as np

def CalcDonchian_High(values, dnchn_span_long):
    dnchnline = pd.Series(values)
    return dnchnline.rolling(window = dnchn_span_long).max()

def CalcDonchian_Low(values, dnchn_span_short):
    dnchnline = pd.Series(values)
    return dnchnline.rolling(window = dnchn_span_short).min()

def CalcATR(phigh, plow, pclose, period):
    high = pd.Series(phigh)
    low = pd.Series(plow)
    close = pd.Series(pclose)
    return ta.ATR(\
        np.array(high).astype("double"),\
        np.array(low).astype("double"),\
        np.array(close).astype("double"),\
        timeperiod=period)

class DnchnBreakout(Strategy):
    dnchn_long = 20
    dnchn_short = 10
    atr_period = 20

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long)
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        if price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.dnchn_low[-2]:
            self.position.close() # 売り

class DnchnBreakout_WithShortPosition(Strategy):
    dnchn_long = 20
    dnchn_short = 10
    atr_period = 20

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long) 
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        if price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.dnchn_low[-2]:
            if not self.position:
                self.sell()
            else:
                self.position.close()

class DnchnBreakout_WithATRStopLoss(Strategy):
    dnchn_long = 40
    dnchn_short = 20
    atr_period = 20
    atr_entrytime = 0

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long)
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): 
        price = self.data.Close[-1]
        atr_entrytime = self.atr[-1]

        if self.position and self.trades[-1].size > 0 and self.trades[-1].entry_price < price - atr_entrytime * 2:
            self.position.close()
        elif self.position and self.trades[-1].size < 0 and self.trades[-1].entry_price > price + atr_entrytime * 2:
            self.position.close()
        elif price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() 
        elif price < self.dnchn_low[-2]:
            self.position.close() 