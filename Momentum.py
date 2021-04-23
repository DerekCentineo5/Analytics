import portfoliolab
from portfoliolab.online_portfolio_selection import *
import pandas as pd
import yfinance as yf
import streamlit as st

def app():
    # Read in data.
    ASSETS = ['AAPL', 'TXN']

    stock_prices = yf.download(ASSETS, start='2018-01-01')

    # Compute Follow the Leader with no given weights.
    ftl = FTL()
    ftl.allocate(asset_prices=stock_prices, resample_by='W', verbose=True)

    # Get the latest predicted weights.
    ftl.weights

    # Get all weights for the strategy.
    ftl.all_weights

    st.write(ftl.portfolio_return)

