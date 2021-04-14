import psycopg2
import psycopg2.extras
import datetime
import streamlit as st
import pandas as pd
import requests
import config
from psaw import PushshiftAPI

def app():

    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'))

    if option == 'twitter':
        for username in config.TWITTER_USERNAMES:
            user = api.get_user(username)
            tweets = api.user_timeline(username)

            st.subheader(username)
            st.image(user.profile_image_url)
            
            for tweet in tweets:
                if '$' in tweet.text:
                    words = tweet.text.split(' ')
                    for word in words:
                        if word.startswith('$') and word[1:].isalpha():
                            symbol = word[1:]
                            st.write(symbol)
                            st.write(tweet.text)
                            st.image(f"https://finviz.com/chart.ashx?t={symbol}")


    if option == 'stocktwits':
        symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)

        r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

        data = r.json()

        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])


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

