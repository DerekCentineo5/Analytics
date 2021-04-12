from portfoliolab.online_portfolio_selection import EG
from PIL import Image
import numpy.core.multiarray
import pandas as pd
import streamlit as st
import datetime as dt
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def app():

    # Title and Image

    st.write("""
    # **Falcon Management Dashboard**
    Risk Ranges Tool
    """)

    # Get User Input

    st.sidebar.header('User Input')

    #### MAYBE ADD IN SOURCE OPTION?????

    def get_input():

        start_date = st.sidebar.text_input("Start Date", "2020-01-01")
        end_date = st.sidebar.text_input("End Date", (dt.datetime.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d"))
        index = st.sidebar.selectbox("Basket", ("Global Indices", "US Sectors","Macrowise Portfolio", "Crypto", "Country ETFs"))
        Momentum = st.sidebar.selectbox("Momentum", ("MU", "GP", "EM", "Follow-the-Leader"))
        Time_Period = st.sidebar.selectbox("Intervals", ("D","W"))
        Learning_Rate = st.sidebar.slider("Learning Rate", min_value=0, max_value=20,value=10, step=.05)

        return start_date, end_date, index, Momentum, Time_Period, Learning_Rate

    def get_data(symbol, Start, End, MTUM, Interval, LR):

        Global_Indices = ['^GSPC', '^IXIC', '^RUT', '^GSPTSE', '^BVSP','^STOXX50E', '^GDAXI','^N225','^HSI','^AXJO']
        US_Sectors = ['XLK','XLP','XLY','XRT','XLI','XLV','XBI','XLB','XLE','XLF','XLC','XLU']
        Macrowise = ['ADI', 'ASML', 'TSM', 'ERIC','NOK','EA','ILMN','INTC','MCHP','COST','MELI','SLV', 'QGEN','EWT','SWKS', 'TXN', 'MSFT', 'CCJ', 'GLD', 'XBI', 'PYPL', 'SQ']
        Crypto = ['BTC-USD', 'ETH-USD', 'DOT1-USD', 'LINK-USD', 'KSM-USD', 'XRP-USD', 'ATOM1-USD', 'ADA-USD']
        Country_ETF = ['SPY','EWC', 'EWW','EWZ', 'ECH', 'EWI','DAX','EWN', 'EWU', 'GREK','TUR','EZA','RSX','INDA','FXI','EWJ','EWY','EWM','EWT','EWA']

        if symbol=="Global Indices":
            Prices = yf.download(Global_Indices, start=Start, end=End)
            MOM = EG(update_rule=MTUM, eta=LR)
            MOM.allocate(asset_prices=MOM['Close'], resample_by=Interval)
            Weights = pd.DataFrame(MOM.all_weights)
        
        return Weights

    start, end, index, mtum, interval_time, learning = get_input()

    Data = get_data(symbol=index, Start=start, End=end, MTUM=mtum, Interval=interval_time, LR=learning)
    Data

    st.header(Momentum + "Momentum")

    st.dataframe(Data)
