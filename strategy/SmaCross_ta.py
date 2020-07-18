from backtesting import Backtest, Strategy
from backtesting.lib import *
from backtesting.test import *
from backtesting import test
import talib.abstract as abstract

class SmaCross(Strategy):
    def init(self):
        Ind = abstract.Function('sma')
        inputs = {
            'open': self.data.Open,
            'high': self.data.High,
            'low': self.data.Low,
            'close': self.data.Close,
            'volume': self.data.Volume
        }
        self.ma1 = self.I(Ind, inputs, 10)
        self.ma2 = self.I(Ind, inputs, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002)
print(bt.run())