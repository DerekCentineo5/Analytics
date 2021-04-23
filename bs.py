import streamlit as st
import alpaca_trade_api as tradeapi
import pandas as pd
import datetime as dt
import config

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

Account = api.get_account()

Account.equity

balance_change = float(Account.equity) - float(Account.last_equity)

Brokerage = pd.DataFrame(columns=['Date', 'Port_Value'], index=['DT'])
for i in Brokerage:
    Account = api.get_account()
    Brokerage[i]=Brokerage.append({'Date': dt.datetime.today(), 'Port_Value': float(Account.equity)}, ignore_index=True)

Brokerage