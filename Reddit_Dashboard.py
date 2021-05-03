import config
import datetime
import sqlite3
import psaw
import config
import streamlit as st
import pandas as pd
from psaw import PushshiftAPI

def app():

    connection = sqlite3.connect(config.DB_FILE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM stock
    """)
    rows = cursor.fetchall()

    stocks = {}
    for row in rows: 
        stocks['$' + row['symbol']] = row['id']

    symbols = {}
    for row in rows:
        symbols['$' + row['symbol']] = row['symbol']

    api = PushshiftAPI()

    def get_intput():

        start_date = st.sidebar.text_input("Start Date", (dt.datetime.today() - dt.timedelta(days=30)).strftime("%Y-%m-%d"))
        end_date = st.sidebar.text_input("End Date", dt.datetime.today().strftime("%Y-%m-%d"))

        return start_date, end_date
    
    def get_data(start, end):

        df = cursor.execute("""
        SELECT * FROM mention""")

        DF = pd.DataFrame(df, columns = ['stock_id', 'symbol', 'date', 'message', 'source', 'url'])
        DF['date'] = pd.to_datetime(DF['date'])  
        mask = (DF['date'] > start) & (DF['date'] <= end)
        DF = DF.loc[mask]
        Counts = pd.DataFrame(DF['symbol'].value_counts())

        return Counts

    Start, End = get_intput()

    Data = get_data(start=Start, end=End)

    st.write(Data)
