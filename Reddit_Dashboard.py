import streamlit as st
import pandas as pd
import numpy as np
import requests
import config
import plotly.graph_objects as go

def app():

    option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'), 3)

    st.header(option)

   if option == 'stocktwits':
        symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)

        r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

        data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
