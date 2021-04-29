import pytrends
from pytrends.request import TrendReq
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import config
import datetime as dt
import streamlit as st

def app():

    st.write("""
        # **Falcon Management Dashboard**
        Google Trends Narrative Tool
        """)

    option = st.sidebar.selectbox("Google Trends Data", ('Top & Rising', 'Historical Trends'), 0)


    if option == 'Top & Rising':
    
        Trending_Terms = TrendReq(hl='en-US', tz=360)

        Keywords = ['stock price']

        Trending_Terms.build_payload(
            kw_list=Keywords,
            cat=0,
            timeframe='now 1-H',
            geo='US',
            gprop='')

        Interest_Over_Time = Trending_Terms.interest_over_time()

        Related_Queries = Trending_Terms.related_queries()

        top_queries=[]
        rising_queries=[]
        for key, value in Related_Queries.items():
            for k1, v1 in value.items():
                if(k1=="top"):
                    top_queries.append(v1)
                elif(k1=="rising"):
                    rising_queries.append(v1)
        top_searched=pd.DataFrame(top_queries[0])
        top_searched['query'] = top_searched['query'].str.split(' ').str[0]
        rising_searched=pd.DataFrame(rising_queries[0])
        rising_searched['query'] = rising_searched['query'].str.split(' ').str[0]

        st.header("Top Trends")
        fig = go.Figure(data=go.Bar(x=top_searched['query'], y=top_searched['value'], name="Trend"))
        fig.update_layout(
            xaxis=dict(title="Trend"),
            yaxis=dict(title="Mentions"),
            )
        st.plotly_chart(fig, use_container_width=True)
        st.header("Rising Trends")
        fig2 = go.Figure(data=go.Bar(x=rising_searched['query'], y=rising_searched['value'], name="Trend"))
        st.plotly_chart(fig2, use_container_width=True)
    
    if option == 'Historical Trends':

        def get_input():

            start_date = st.sidebar.text_input("Start Date", (dt.datetime.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d"))
            end_date = st.sidebar.text_input("End Date", (dt.datetime.today()).strftime("%Y-%m-%d"))
            #Specific_Security_Option = st.sidebar.selectbox("Specific Trend?", ("Yes", "No"))
            #symbol = st.sidebar.text_input("Trend or ")

            return start_date, end_date

        def get_data(Start, End):

            Trending_Terms = TrendReq(hl='en-US', tz=360)

            Keywords = ['share price','stock price', 'price']

            Trending_Terms.build_payload(
            kw_list=Keywords,
            cat=0,
            timeframe=f'{Start} {End}',
            geo='US',
            gprop='')

            Interest_Over_Time = Trending_Terms.interest_over_time()
            Related_Queries = Trending_Terms.related_queries()

            top_queries=[]
            rising_queries=[]
            for key, value in Related_Queries.items():
                for k1, v1 in value.items():
                    if(k1=="top"):
                        top_queries.append(v1)
                    elif(k1=="rising"):
                        rising_queries.append(v1)
            top_searched=pd.DataFrame(top_queries[1])
            rising_searched=pd.DataFrame(rising_queries[1])

            return top_searched, rising_searched

        start, end = get_input()

        TOP, RISING = get_data(Start=start, End=end)

        st.header("Top Trends")
        st.dataframe(TOP)

        st.header("Rising Trends")
        st.dataframe(RISING)
        
#############################
#connection = sqlite3.connect(config.DB_FILE)

#connection.row_factory = sqlite3.Row

#cursor = connection.cursor()

#cursor.execute("""
#    SELECT id, symbol, name FROM stock
#""")

#rows = cursor.fetchall()

#symbols = []
#names = []
#stock_dict = {}
#for row in rows:
    #symbol = row['symbol']
    #name = row['name']
    #symbols.append(symbol)
    #names.append(name)
    #stock_dict[symbol] = row['id']
#df=pd.DataFrame(symbols, columns=['Symbol'])
#df['Name'] = names
#df



