import os
import sys
import Jim_Dash
import Alpaca_Feed
import Reddit_Dashboard
import Falcon_Management_Ranges
import streamlit as st
from PIL import Image

PAGES = {
    "Daily Ranges": Jim_Dash,
    "Risk Ranges Analysis": Falcon_Management_Ranges,
    "Algorithm": Alpaca_Feed,
    'Social Media Sentiment': Reddit_Dashboard
    #"Social Media Sentiment": Reddit_Screener
}

Falcon = Image.open("Falcon.jpeg")
st.sidebar.image(Falcon, use_column_width=False)
st.sidebar.title('Dashboard Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()



