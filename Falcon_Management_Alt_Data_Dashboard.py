import os
import sys
import Mom
import Jim_Dash
import Falcon_Management_Ranges
import streamlit as st
from PIL import Image

PAGES = {
    "Momentum": Mom,
    "Daily Ranges": Jim_Dash,
    "Risk Ranges Analysis": Falcon_Management_Ranges
}

Falcon = Image.open("Falcon.jpeg")
st.sidebar.image(Falcon, use_column_width=False)
st.sidebar.title('Dashboard Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()



