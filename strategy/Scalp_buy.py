from backtesting import Backtest, Strategy, Position,Order
from backtesting.lib import crossover, SignalStrategy
from backtesting.test import SMA
from backtesting.test import ES
# Refer https://github.com/kernc/backtesting.py/pull/47
class Scalp_buy(Strategy):
    start = 125
    lot_step = 5
    buy_criteria = 1
    sell_criteria = 1
    max_open = 10
    lot_size = 6000
    max_loss = 1000
    equity_list = []
    current_buy_order = []
    current_sell_order = []
    current_buy = start - buy_criteria
    current_sell = start + sell_criteria

    def init(self):
        super().init()
        self.current_buy = self.start - self.buy_criteria
        self.current_sell = self.start + self.sell_criteria
        self.buy(limit = self.start, tp = self.current_sell)

    def next(self):
        super().next()
        for x in range(0,self.max_open):
            # self.order_api.set_entry(price = self.current_buy)
            # self.order_api.set_tp(price = self.current_sell)
            self.buy(limit = self.current_buy,tp=self.current_sell)
            self.current_buy  += self.buy_criteria
            self.current_sell  += self.sell_criteria
        print(self.position.pl, self.position.pl_pct , self.position.size)

bt = Backtest(ES, Scalp_buy, cash=10000, commission=.0014)
output = bt.run()
print(output)
