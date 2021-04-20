import config
import sqlite3
import psycopg2
import psycopg2.extras
import datetime
import streamlit as st
import pandas as pd
import requests

def app():

    connection = sqlite3.connect(config.DB_FILE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()    

    option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'))


    if option == 'wallstreetbets':
            num_days = st.sidebar.slider('Number of days', 1, 30, 3)

            cursor.execute("""
                SELECT COUNT(*) AS num_mentions, symbol
                FROM mention JOIN stock ON stock.id = mention.stock_id
                WHERE date(dt) > current_date - interval '%s day'
                GROUP BY stock_id, symbol   
                HAVING COUNT(symbol) > 10
                ORDER BY num_mentions DESC
            """, (num_days,))

            counts = cursor.fetchall()
            for count in counts:
                st.write(count)

            cursor.execute("""
                SELECT symbol, message, url, dt
                FROM mention JOIN stock ON stock.id = mention.stock_id
                ORDER BY dt DESC
                LIMIT 100
            """)

            mentions = cursor.fetchall()
            for mention in mentions:
                st.text(mention['dt'])
                st.text(mention['symbol'])
                st.text(mention['message'])
                st.text(mention['url'])
                #st.text(mention['username'])

            rows = cursor.fetchall()

            st.write(rows)
