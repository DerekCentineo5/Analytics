import pandas as pd
import config
import alpaca_trade_api as tradeapi
import datetime
import numpy as np
import yfinance as yf
import streamlit as st
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

    Output = pd.DataFrame(Final_Bottom).rename(columns={0:'Bottom RR'})

    Output['Top RR'] = Final_Top
    Output['Mid RR'] = Final_Mid
    Output['Trend'] = Trend
    Output['Price'] = Close
    Output = Output.dropna()
    
    return Output

print(datetime.now())

symbols = ['ADI', 'ASML', 'TSM', 'ERIC','NOK','EA','ILMN','INTC','MCHP','COST', 'CRSP', 'INO']

current_date = date.today().isoformat()
current_date

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

Bars = {}
RR={}
for symbol in symbols:
    Bars[symbol] = yf.download(symbol, start='2020-09-01', end=current_date)
    RR[symbol] = RiskRange(Bars[symbol])
    if RR[symbol].Bottom_RR.values[-1] > RR[symbol].Price.values[-1]:

        api.submit_order(
            symbol=symbol,
            qty=3,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            stop_loss={'stop_price': (RR[symbol].Bottom_RR.values[-1])*.90},
            take_profit={'limit_price': (RR[symbol].Price.values[-1])*1.05}
        )   


