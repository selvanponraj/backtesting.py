from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG,ES, SMA


class SmaCross(Strategy):

    def init(self):
        setattr(self, "sma1", self.I(SMA, self.data.Close, getattr(self, "n1")))
        setattr(self, "sma2", self.I(SMA, self.data.Close, getattr(self, "n2")))

    def next(self):
        if crossover(getattr(self, "sma1"), getattr(self, "sma2")):
            self.buy()
        elif crossover(getattr(self, "sma2"), getattr(self, "sma1")):
            self.sell()


def prepare_optimization(cls: type) -> dict:
    # Set the class variables upon the class
    setattr(cls, 'n1', 1)
    setattr(cls, 'n2', 2)
    # Construct and return optimization kwargs
    return {'n1': range(5, 30, 5),
            'n2': range(10, 70, 5),
            'constraint': lambda p: p['n1'] < p['n2'],
            'maximize': 'Equity Final [$]'}


bt = Backtest(ES, SmaCross, cash=10000, commission=.002, exclusive_orders=True)
opt_kwargs = prepare_optimization(SmaCross)
x = bt.optimize(**opt_kwargs)
print(x.to_string())