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
#from zipline.api import order_target, symbol, order, order_percent, order_target_percent
#from zipline.data import bundles
#from zipline.utils.calendars import get_calendar
#from zipline import run_algorithm
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

    Falcon = Image.open("Falcon.jpeg")
    st.sidebar.image(Falcon, use_column_width=False)
    st.sidebar.header('User Input')

    # Get User Input

    #### MAYBE ADD IN SOURCE OPTION?????

    def get_input():

        start_date = st.sidebar.text_input("Start Date", "2018-01-01")
        end_date = st.sidebar.text_input("End Date", dt.datetime.today().strftime("%Y-%m-%d"))
        stock_symbol = st.sidebar.text_input("Yahoo Finance Symbol", "QQQ")
        volume_weighted = st.sidebar.selectbox("Volume Weigthed", (True, False))
        trade_period = st.sidebar.slider("Trade Period", min_value=2, max_value=21,value=10, step=1)
        trend_period = st.sidebar.slider("Trend Period", min_value=60, max_value=130,value=63, step=1)

        return start_date, end_date, stock_symbol, volume_weighted, trade_period, trend_period

    def get_data(symbol, Start, End):

        Data = yf.download(symbol, start=Start, end=End)

        return Data

    #Get Data
    start, end, symbol, vw, trade, trend = get_input()

    Data = get_data(symbol=symbol, Start=start, End=end)

    #Calculate Risk Ranges
    RR = RiskRange(Price_Data=Data, window=trade, length=trend, volume_weighted=vw, vol_window=trade)

    ############################################################ Display ############################################################

    Company_Name = yf.Ticker(symbol).info['shortName']

    st.header(Company_Name +" Risk Ranges\n")

    fig = go.Figure(data=go.Scatter(x=RR.index, y=RR['Trend'], name="Trend"))

    fig.add_trace(go.Scatter(x=RR.index, y=RR['Bottom RR'], name='Bottom Risk Range'))

    fig.add_trace(go.Scatter(x=RR.index, y=RR['Top RR'], name='Top Risk Range'))

    fig.add_trace(go.Candlestick(x=Data.index,open=Data['Open'], high=Data['High'], low=Data['Low'], close=Data['Close'], name=(symbol +" Price\n")))

    fig.update_layout(
        autosize=False,
        width=700,
        height=400, margin=dict(l=0, r=10, t=58, b=0), 
        legend=dict(orientation="h",yanchor="bottom",y=1,xanchor="left",x=0))

    st.plotly_chart(fig, use_container_width=False)

    st.write(RR)

