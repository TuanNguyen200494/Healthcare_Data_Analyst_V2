import streamlit as st
import pandas as pd

from app.ui.configure_page_sidebar import render_sidebar_configure_page
from app.ui.configure_page_sidebar_rawdataconfig import configure_session_state, render_for_rawdataconfig


st.set_page_config(
    page_title="Configuration",
    layout = "wide"
)

select = render_sidebar_configure_page()
configure_session_state()

if (select == "Raw Data Configure"):
    render_for_rawdataconfig()
