import os
import sys
import Jim_Dash
import Falcon_Management_Ranges
import streamlit as st
from PIL import Image
sys.path.insert(0, '/Users/derekcentineo/Documents/GitHub/Momentum')
import Main_Momentum

PAGES = {
    "Daily Ranges": Jim_Dash,
    "Risk Ranges Analysis": Falcon_Management_Ranges,
    "Momentum": Main_Momentum
}

Falcon = Image.open("Falcon.jpeg")
st.sidebar.image(Falcon, use_column_width=False)
st.sidebar.title('Dashboard Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()



