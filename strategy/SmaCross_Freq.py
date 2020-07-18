from backtesting import Backtest, Strategy
from backtesting.lib import *
from backtesting.test import *
from backtesting import test

from pandas import DataFrame
import talib.abstract as ta
from user_data.strategies.berlinguyinca import *
import numpy as np  # noqa

ES= test._read_file('04_ESU2020_FUT.csv')

class SmaCross_Freq(Strategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['maShort'] = ta.SMA(dataframe, timeperiod=25)
        dataframe['maMedium'] = ta.SMA(dataframe, timeperiod=60)
        return dataframe

    def init(self):

        # For Freq Strategy
        self.data.df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'},
                  inplace=True)
        self.strategy = AverageStrategy.AverageStrategy(None)
        self.populate_indicators(self.data.df,None)
        self.strategy.populate_buy_trend(self.data.df, None)
        self.strategy.populate_sell_trend(self.data.df, None)

        # Back to Backtesting
        self.data.df.rename(
            columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'Volume': 'volume'},
            inplace=True)

        # Verification
        print(self.data.df.dropna(subset=['buy', 'sell'], how='all').tail(5))

    def next(self):
        if not np.isnan(self.data.df['buy'].iloc[-1]):
            self.position.close()
            self.buy()
        elif not np.isnan(self.data.df['sell'].iloc[-1]):
            self.position.close()
            self.sell()

    def next_1(self):
        pass
        # if self.indicators['sma1'].crossed_above(self.data.df['sma2']):
        #     # if qtpylib.crossed_above(self.indicators['maShort'], self.indicators['maMedium']):
        #     self.position.close()
        #     self.buy()
        # elif self.data.df['sma2'].crossed_above(self.data.df['sma1']):
        #     self.position.close()
        #     self.sell()

        # if not np.isnan(self.sell_signal['buy'].iloc[-1]):
        #     self.position.close()
        #     self.buy()
        # elif not np.isnan(self.sell_signal['sell'].iloc[-1]):
        #     self.position.close()
        #     self.sell()

        # if crossover(self.data.df['maShort'], self.data.df['maMedium']):
        #     self.position.close()
        #     self.buy()
        #
        # # Else, if sma1 crosses below sma2, close any existing
        # # long trades, and sell the asset
        # elif crossover(self.data.df['maMedium'], self.data.df['maShort']):
        #     self.position.close()
        #     self.sell()

        # if not np.isnan(self.signal['buy'].iloc[-1]):
        #     self.position.close()
        #     self.buy()
        # elif not np.isnan(self.signal['sell'].iloc[-1]):
        #     self.position.close()
        #     self.sell()
        # print('End')

        # if not instrument.pending_orders and positions["position"] == 0:
        #     if direction is not None and direction == 'BUY':
        #         instrument.buy(1)
        #         self.record(TD_SS_BUY=1)
        #     elif direction is not None and direction == 'SELL':
        #         instrument.sell(1)
        #         self.record(TD_SS_SELL=1)

        # # If sma1 crosses above sma2, close any existing
        # # short trades, and buy the asset
        # if crossover(self.data.df['sma1'], self.data.df['sma2']):
        #     self.position.close()
        #     self.buy()
        #
        # # Else, if sma1 crosses below sma2, close any existing
        # # long trades, and sell the asset
        # elif crossover(self.data.df['sma2'], self.data.df['sma1']):
        #     self.position.close()
        #     self.sell()

    # def init(self):
    #     df = self.data.df.copy(deep=True)
    #
    #     df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'},
    #            inplace=True)
    #
    #     # print(df.tail(2))
    #     # import pandas_ta as ta
    #
    #     self.ma1 = self.I(SMA, self.data.Close, 10)
    #     self.ma2 = self.I(SMA, self.data.Close, 20)
    #
    #     # self.data.df.ta.sma(length=10, append=True)
    #
    #
    #     # uses close prices (default)
    #
    #
    #     self.data.df['short'] = ta.SMA(df, timeperiod=10)
    #     self.data.df['medium'] = ta.SMA(df, timeperiod=20)
    #
    #     # self.ma11= self.ma101
    #     # self.ma22=self.ma102
    #
    #
    #
    #     # self.indicators = s.populate_indicators(ES, None)
    #     # # print(self.indicators)
    #     # self.buy_trend = s.populate_buy_trend(self.indicators, None)
    #     # print(self.buy_trend)
    #
    #     # ES['maShort'] = ta.SMA(ES, timeperiod=10)
    #     # ES['maMedium'] = ta.SMA(ES, timeperiod=20)
    #
    #     #
    #     # self.ma1 = ta.SMA(self.data., timeperiod=10)
    #     #
    #     # # uses open prices
    #     # self.ma2 = ta.SMA(self.data.to_series(), timeperiod=20)
    #
    #     # ES['ema100'] = ta.EMA(ES, timeperiod=100)
    #
    #     # self.ma1 = ta.SMA(ES, timeperiod=10)
    #     # self.ma2 = ta.SMA(ES, timeperiod=20)
    #
    #
    #     # self.ma1 = resample_apply("15Min", SMA, Close, 10)
    #     # self.ma2 = resample_apply("15Min", SMA, Close, 20)
    #
    #
    # def next(self):
    #     # if qtpylib.crossed_above(self.data.df['short'],self.data.df['medium']):
    #     #     self.buy()
    #     # elif qtpylib.crossed_above(self.data.df['medium'],self.data.df['short']):
    #     #     self.sell()
    #
    #     if crossover(self.ma1,self.ma2):
    #         self.buy()
    #     elif crossover(self.ma2,self.ma1):
    #         self.sell()

rule = '15Min'
ES = ES.resample(rule='15Min', label='right').agg(OHLCV_AGG).dropna()
bt = Backtest(ES, SmaCross_Freq,
              cash=10000, commission=.002)

print(bt.run())
# bt.plot()