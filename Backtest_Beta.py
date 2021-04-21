import pandas as pd
import backtesting
import numpy as np
import yfinance as yf
import streamlit as st
from ta.volatility import average_true_range
from pandas_ta.overlap import vwma
from pandas_ta.overlap import wma
from backtesting import Strategy
from backtesting import Backtest
from backtesting.lib import crossover
from backtesting.test import GOOG, SMA

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

def app():

    def get_input():

        start_date = st.sidebar.text_input("Start Date", "2018-01-01")
        end_date = st.sidebar.text_input("End Date", (dt.datetime.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d"))
        stock_symbol = st.sidebar.text_input("Yahoo Finance Symbol", "QQQ")
        volume_weighted = st.sidebar.selectbox("Volume Weighted", (True, False))
        trade_period = st.sidebar.slider("Trade Period", min_value=2, max_value=21,value=10, step=1)
        trend_period = st.sidebar.slider("Trend Period", min_value=60, max_value=130,value=63, step=1)

        return start_date, end_date, stock_symbol, volume_weighted, trade_period, trend_period

    def get_data(symbol, Start, End):

        Data = yf.download(symbol, start=Start, end=End)

        return Data

    start, end, symbol, vw, trade, trend = get_input()

    Data = get_data(symbol=symbol, Start=start, End=end)
    
    df = RiskRange(Data, window=trade, length=trend, volume_weighted=vw, vol_window=trade)
    Data['BOTTOM_RR'] = df.Bottom_RR
    Data['TREND'] = df.Trend
    Data['TOP_RR'] = df.Top_RR 
    Data = Data.dropna()

    class Ranges(Strategy):
        # Define the two MA lags as *class variables*
        # for later optimization

        def init(self):
            # Precompute the two moving averages
            self.data.BOTTOM_RR
            self.data.TREND
            self.data.Close
            self.data.TOP_RR
        
        def next(self):
            if crossover(self.data.BOTTOM_RR, self.data.Close):
                self.buy()
            elif crossover(self.data.Close, self.data.TOP_RR):
                self.position.close()
            elif crossover(self.data.TREND, self.data.BOTTOM_RR):
                self.position.close()
                #self.buy()


    bt = Backtest(Data, Ranges, commission=.002,
                exclusive_orders=True)
        
    stats = bt.run()

    Returns_Plot = bt.plot(plot_return=True)

    raw_html = Returns_Plot._repr_html_()

    st.components.v1.html(raw_html)

    st.table(stats)
