import sqlite3
import config
from Jim_Dash import RiskRange
import pandas as pd
import yfinance as yf
import streamlit as st
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import datetime as dt

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

orders = api.list_orders()
existing_order_symbols = [order.symbol for order in orders]

current_date = (dt.datetime.today() + dt.timedelta(days=1))
beginning_date = '2020-07-01'

symbols = ['ADI', 'TSM', 'MCHP', 'TXN', 'ASML', 'PYPL', 'SQ', 'TMO', 'ILMN','QGEN','EWT', 'EWJ', 'EWZ',
            'GLD','SLV', 'TMUS', 'CCJ', 'MSFT', 'SWKS', 'MELI', 'EA', 'ERIC', 'NOK', 'COST', 'INTC']

for symbol in symbols:
    
    Prices = pd.DataFrame(yf.download(symbol, start=beginning_date, end=current_date))
    RR = RiskRange(Price_Data=Prices, window=10, length=63, volume_weighted=True, vol_window=10)

    RR_Bottom = RR['Bottom RR'][-1]
    RR_Top = RR['Top RR'][-1]
    RR_Trend = RR['Trend'][-1]
    Price = RR['Price'][-1]

    Near_Bottom = RR_Bottom*1.01
    Near_Top = RR_Top*0.995

    if RR_Bottom > RR_Trend:
        if symbol not in existing_order_symbols:
            
            print(symbol)

            Account = api.get_account()

            Target_QTY = int((float(Account.equity)*0.03)/Price)

            api.submit_order(
            symbol=symbol,
            qty=Target_QTY,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            stop_loss={'stop_price': RR_Trend},
            take_profit={'limit_price': Near_Top * 1.01}
            )   

    elif Price < Near_Bottom:
        if symbol not in existing_order_symbols:
            
            print(symbol)

            Account = api.get_account()

            Target_QTY = int((float(Account.equity)*0.03)/Price)

            api.submit_order(
            symbol=symbol,
            qty=Target_QTY,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            stop_loss={'stop_price': RR_Bottom*.90},
            take_profit={'limit_price': RR_Top *.995}
            )   


