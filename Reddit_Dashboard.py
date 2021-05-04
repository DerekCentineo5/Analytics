import config
import datetime
import sqlite3
import datetime as dt
import config
import streamlit as st
import pandas as pd

def app():

    connection = sqlite3.connect('C:\\Users\derekcentineo\Documents\GitHub\Analytics\app.db')

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

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
