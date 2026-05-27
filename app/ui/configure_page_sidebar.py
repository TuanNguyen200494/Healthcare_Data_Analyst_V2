import streamlit as st

def render_sidebar_configure_page():
    with st.sidebar:
        st.title("Configuration")

        select = st.radio("Config Option", options=["Raw Data Configure", "API Key Configure", "Export Configure"])
        return select
                          