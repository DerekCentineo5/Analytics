import pytrends
from pytrends.request import TrendReq
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def app():

    st.write("""
    # **Falcon Management Dashboard**
    Google Trends Narrative Tool
    """)

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