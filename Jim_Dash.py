import os
import pandas as pd
from PIL import Image
import streamlit as st
import datetime as dt
import yfinance as yf
import pandas_ta as pta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.volatility import average_true_range
from pandas_ta.overlap import vwma
from pandas_ta.overlap import wma
import pandas_datareader as pdr 
import ta
import numpy as np

def RiskRange(Price_Data, window=10, length=63, volume_weighted=True, vol_window=5, mindiff=100000000.0, maxdiff=-100000000.0):
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

### For Multi-Tab!!!!!

def app():

    # Title and Image

    st.write("""
    # **Falcon Management Dashboard**
    Risk Ranges Tool
    """)
    # Sidebar Header

    st.sidebar.header('User Input')

    # Get User Input

    #### MAYBE ADD IN SOURCE OPTION?????

    def get_input():

        start_date = st.sidebar.text_input("Start Date", "2018-01-01")
        end_date = st.sidebar.text_input("End Date", (dt.datetime.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d"))
        index = st.sidebar.selectbox("Indexes or Portfolio", ("Global Indices", "US Sectors","Macrowise Portfolio", "Crypto", "Country ETFs"))
        volume_weighted = st.sidebar.selectbox("Volume Weighted", (True, False))
        trade_period = st.sidebar.slider("Trade Period", min_value=2, max_value=21,value=10, step=1)
        trend_period = st.sidebar.slider("Trend Period", min_value=60, max_value=130,value=63, step=1)

        return start_date, end_date, index, volume_weighted, trade_period, trend_period

    def get_data(symbol, Start, End, Trade, Trend, VW):

        Global_Indices = ['^GSPC', '^IXIC', '^RUT', '^GSPTSE', '^BVSP','^STOXX50E', '^GDAXI','^N225','^HSI','^AXJO']
        US_Sectors = ['XLK','XLP','XLY','XRT','XLI','XLV','XBI','XLB','XLE','XLF','XLC','XLU']
        Macrowise = ['ADI', 'ASML', 'TSM', 'ERIC','NOK','EA','ILMN','INTC','MCHP','COST','MELI','SLV', 'QGEN','EWT','SWKS', 'TXN', 'MSFT', 'CCJ', 'GLD', 'XBI', 'PYPL', 'SQ']
        Crypto = ['BTC-USD', 'ETH-USD', 'DOT1-USD', 'LINK-USD', 'KSM-USD', 'XRP-USD', 'ATOM1-USD', 'ADA-USD']
        Country_ETF = ['SPY','EWC', 'EWW','EWZ', 'ECH', 'EWI','DAX','EWN', 'EWU', 'GREK','TUR','EZA','RSX','INDA','FXI','EWJ','EWY','EWM','EWT','EWA']


        if symbol=="Global Indices":
            Data = {}
            New_Data = pd.DataFrame()
            for i in Global_Indices:
                Data[i] = pd.DataFrame(yf.download(i, start=Start,end=End))
            for  i, df in Data.items():
                Data[i] = pd.DataFrame(RiskRange(Price_Data=df, window=Trade, length=Trend, volume_weighted=VW, vol_window=Trade))
                Data[i] = pd.DataFrame(Data[i])[-1:]
                Data[i].insert(1, 'Asset', i)
                #Data[i].set_index('Asset')
                New_Data = New_Data.append(Data[i], ignore_index=True)
                Final = New_Data.set_index('Asset')
                Matrix = Final[['Price', 'Trend', 'Bottom RR', 'Top RR','Mid RR']]

        elif symbol=="US Sectors":
            Data = {}
            New_Data = pd.DataFrame()
            for i in US_Sectors:
                Data[i] = pd.DataFrame(yf.download(i, start=Start,end=End))
            for  i, df in Data.items():
                Data[i] = pd.DataFrame(RiskRange(Price_Data=df, window=Trade, length=Trend, volume_weighted=VW, vol_window=Trade))
                Data[i] = pd.DataFrame(Data[i])[-1:]
                Data[i].insert(1, 'Asset', i)
                #Data[i].set_index('Asset')
                New_Data = New_Data.append(Data[i], ignore_index=True)
                Final = New_Data.set_index('Asset')
                Matrix = Final[['Price', 'Trend', 'Bottom RR', 'Top RR','Mid RR']]
        
        elif symbol=="Macrowise Portfolio":
            Data = {}
            New_Data = pd.DataFrame()
            for i in Macrowise:
                Data[i] = pd.DataFrame(yf.download(i, start=Start,end=End))
            for  i, df in Data.items():
                Data[i] = pd.DataFrame(RiskRange(Price_Data=df, window=Trade, length=Trend, volume_weighted=VW, vol_window=Trade))
                Data[i] = pd.DataFrame(Data[i])[-1:]
                Data[i].insert(1, 'Asset', i)
                #Data[i].set_index('Asset')
                New_Data = New_Data.append(Data[i], ignore_index=True)
                Final = New_Data.set_index('Asset')
                Matrix = Final[['Price', 'Trend', 'Bottom RR', 'Top RR','Mid RR']]
            
        elif symbol=="Crypto":
            Data = {}
            New_Data = pd.DataFrame()
            for i in Crypto:
                Data[i] = pd.DataFrame(yf.download(i, start=Start,end=End))
            for  i, df in Data.items():
                Data[i] = pd.DataFrame(RiskRange(Price_Data=df, window=Trade, length=Trend, volume_weighted=VW, vol_window=Trade))
                Data[i] = pd.DataFrame(Data[i])[-1:]
                Data[i].insert(1, 'Asset', i)
                #Data[i].set_index('Asset')
                New_Data = New_Data.append(Data[i], ignore_index=True)
                Final = New_Data.set_index('Asset')
                Matrix = Final[['Price', 'Trend', 'Bottom RR', 'Top RR','Mid RR']]
        
        elif symbol=="Country ETFs":
            Data = {}
            New_Data = pd.DataFrame()
            for i in Country_ETF:
                Data[i] = pd.DataFrame(yf.download(i, start=Start,end=End))
            for  i, df in Data.items():
                Data[i] = pd.DataFrame(RiskRange(Price_Data=df, window=Trade, length=Trend, volume_weighted=VW, vol_window=Trade))
                Data[i] = pd.DataFrame(Data[i])[-1:]
                Data[i].insert(1, 'Asset', i)
                #Data[i].set_index('Asset')
                New_Data = New_Data.append(Data[i], ignore_index=True)
                Final = New_Data.set_index('Asset')
                Matrix = Final[['Price', 'Trend', 'Bottom RR', 'Top RR','Mid RR']]
                
        return Matrix

    #Get Data
    start, end, index, vw, trade, trend = get_input()

    Data = get_data(symbol=index, Start=start, End=end, Trade=trade, Trend=trend, VW=vw)
    Data

    #Calculate Risk Ranges
    
    ############################################################ Display ############################################################

    #Company_Name = yf.Ticker(symbol).info['shortName']

    #st.header(Company_Name +" Risk Ranges\n")

    st.header("Risk Ranges")

    st.dataframe(Data)
