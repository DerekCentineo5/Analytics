import pytrends
from pytrends.request import TrendReq
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
import streamlit as st

Trending_Terms = TrendReq(hl='en-US', tz=360)
Keywords = ['share price','stock price', 'price']

start = dt.datetime(2017, 1, 1).strftime("%Y-%m-%d")
end ='2018-07-01'

Trending_Terms.build_payload(
            kw_list=Keywords,
            cat=0,
            timeframe=f'{start} {end}',
            geo='US',
            gprop='')

Trending_Terms.get_historical_interest(keywords=Keywords, year_start=2018, month_start=1, day_start=1,
                                        year_end=2018, month_end=1, day_end=20, cat=0, geo='', gprop='', sleep=60)
                                    

Interest_Over_Time = Trending_Terms.interest_over_time()
Interest_Over_Time

Related_Queries = Trending_Terms.related_queries()
Related_Queries





def app():

    st.write("""
        # **Falcon Management Dashboard**
        Google Trends Narrative Tool
        """)

    option = st.sidebar.selectbox("Google Trends Data", ('Top & Rising', 'Historical Trends', 'stocktwits', 'chart', 'pattern'), 0)


    if option == 'Top & Rising':
    
        Trending_Terms = TrendReq(hl='en-US', tz=360)

        Keywords = ['share price','stock price']

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
        top_searched=pd.DataFrame(top_queries[1])
        top_searched
        rising_searched=pd.DataFrame(rising_queries[1])
        rising_searched

        st.write(top_searched)

        st.write(rising_searched)
    
    if option == 'Historical Trends':

        def get_input():

        start_date = st.sidebar.text_input("Start Date", "2018-01-01")
        end_date = st.sidebar.text_input("End Date", (dt.datetime.today()).strftime("%Y-%m-%d"))
        #Specific_Security_Option = st.sidebar.selectbox("Specific Trend?", ("Yes", "No"))
        #symbol = st.sidebar.text_input("Trend or ")
        trade_period = st.sidebar.slider("Trade Period", min_value=2, max_value=21,value=10, step=1)
        trend_period = st.sidebar.slider("Trend Period", min_value=60, max_value=130,value=63, step=1)

        return start_date, end_date

        def get_data(Start, End):

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

        Data = get_data(Start=start, End=end)

        st.writ(Data)
        


