from backtesting import Backtest, Strategy
from backtesting.lib import *
from backtesting.test import *

from backtesting._util import _as_str
from backtesting import test
import talib
import qtpylib.tools as tools

def resample(rule,series,*args,agg='last'):
    resampled = series.resample(rule, label='right').agg(agg).dropna()
    resampled.name = _as_str(series) + '[' + rule + ']'
    return resampled


ES = test._read_file('04_ESU2020_FUT.csv')
# ES.resample('4H', label='right').agg(OHLCV_AGG)
# ES = ES.resample('15Min', label='right').agg(OHLCV_AGG).dropna()

print(ES.tail(5))


class SmaCross(Strategy):
    def init(self):
        # Precompute the two moving averages
        # self.sma1 = self.I(SMA, self.data.Close, 10)
        # self.sma2 = self.I(SMA, self.data.Close, 20)

        # self.sma1 = self.I(talib.SMA, self.data.Close, 10)
        # self.sma2 = self.I(talib.SMA, self.data.Close, 20)

        self.sma1 = resample_apply('15Min', SMA, self.data.Close, 10)
        self.sma2 = resample_apply('15Min', SMA, self.data.Close, 20)

        # resampled_ind = resample_apply('W', SMA, self.sma, 3)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

bt = Backtest(ES, SmaCross,
              cash=10000, commission=.002)

print(bt.run())
# bt.plot()