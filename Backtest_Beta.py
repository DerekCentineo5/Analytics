import pandas as pd
import backtesting
import numpy as np
import yfinance as yf
import streamlit as st
from datetime import datetime
import backtrader as bt
from ta.volatility import average_true_range
from pandas_ta.overlap import vwma
from pandas_ta.overlap import wma

def RiskRange(Price_Data, window=10, length=63, volume_weighted=True, vol_window=10, mindiff=100000000.0, maxdiff=-100000000.0):
    """
    Function to Calculate Risk Ranges
    
    """

    Windowminus1 = window - 1
    
    Close = (Price_Data[['Close']]).dropna()
    
    High = (Price_Data[['High']]).dropna()
    
    Low = (Price_Data[['Low']]).dropna()

    Volume = (Price_Data[['Volume']]).dropna()
    
    Slope = (Close.apply(func = lambda x: x - (x.shift(Windowminus1)))/(Windowminus1)).dropna()
    
    for i in range(0, Windowminus1):
        Min = np.minimum(mindiff, Close.apply(func = lambda x: x.shift(Windowminus1-i) - (x.shift(Windowminus1) + (Slope['Close']*i)), axis=0))
    for i in range(0, Windowminus1):
        Max = np.maximum(maxdiff, Close.apply(func = lambda x: x.shift(Windowminus1-i) - (x.shift(Windowminus1) + (Slope['Close']*i)), axis=0))

    BridgeBottom = (Close + Min).dropna()

    BridgeTop = (Close + Max).dropna()

    ATR = average_true_range(High['High'], Low['Low'], Close['Close'], window=window).dropna()

    Hurst = ((np.log(pd.DataFrame.rolling(High['High'], window=window).max() - pd.DataFrame.rolling(Low['Low'], window=window).min()) - np.log(ATR))/(np.log(window)))

    Hurst_New = pd.DataFrame(Hurst.values, index=Hurst.index).rename(columns={0:'Hurst'})

    SD = (Close['Close']).rolling(vol_window).std()

    if volume_weighted==True:
        WMA = vwma(Close['Close'], Volume['Volume'], length=vol_window)
    elif volume_weighted==False:
        WMA = wma(Close['Close'], length=vol_window)

    BBBottom = (WMA - (SD*2)).dropna()

    BBTop = (WMA + (SD*2)).dropna()

    Final_Bottom = BBBottom +((BridgeBottom['Close'] - BBBottom) * np.abs((Hurst_New['Hurst']*2)-1))

    Final_Top = BBTop + ((BridgeTop['Close'] - BBTop) * np.abs((Hurst_New['Hurst']*2)-1))

    Final_Mid = Final_Bottom + ((Final_Top - Final_Bottom)/2)

    Trend = ((pd.DataFrame.rolling(Low['Low'], window=length).min()) + ((pd.DataFrame.rolling(High['High'], window=length).max() - pd.DataFrame.rolling(Low['Low'], window=length).min())/2))

    Output = pd.DataFrame(Final_Bottom).rename(columns={0:'Bottom_RR'})

    Output['Top_RR'] = Final_Top
    Output['Mid_RR'] = Final_Mid
    Output['Trend'] = Trend
    Output['Price'] = Close
    Output = Output.dropna()
    
    return Output


class DonchianChannels(bt.Indicator):
    '''
    Params Note:
      - `lookback` (default: -1)
        If `-1`, the bars to consider will start 1 bar in the past and the
        current high/low may break through the channel.
        If `0`, the current prices will be considered for the Donchian
        Channel. This means that the price will **NEVER** break through the
        upper/lower channel bands.
    '''

    alias = ('DCH', 'DonchianChannel',)

    lines = ('dcm', 'dch', 'dcl',)  # dc middle, dc high, dc low
    params = dict(
        period=20,
        lookback=-1,  # consider current bar or not
    )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        dcm=dict(ls='--'),  # dashed line
        dch=dict(_samecolor=True),  # use same color as prev line (dcm)
        dcl=dict(_samecolor=True),  # use same color as prev line (dch)
    )

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        self.l.dcl = bt.ind.Lowest(lo, period=self.p.period)
        self.l.dcm = (self.l.dch + self.l.dcl) / 2.0  # avg of the above


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.myind = DonchianChannels()

    def next(self):
        if self.data[0] > self.myind.dch[0]:
            self.buy()
        elif self.data[0] < self.myind.dcl[0]:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(1337.0)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                     fromdate=datetime(2010, 1, 1),
                                     todate=datetime(2017, 12, 31))
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')

    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    if args.printout:
        print('-- RETURNS')
        print(returns)
        print('-- POSITIONS')
        print(positions)
        print('-- TRANSACTIONS')
        print(transactions)
        print('-- GROSS LEVERAGE')
        print(gross_lev)

    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        transactions=transactions,
        gross_lev=gross_lev,
        live_start_date='2010-01-01',
        round_trips=True)