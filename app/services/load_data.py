import pandas as pd
import streamlit as st

from app.config.paths import find_root_project

@st.cache_data
def load_data(file_name:str):
    root = find_root_project()
    data_dir = root / "data"
    raw_dir = data_dir / "raw"

    target_file = raw_dir / file_name

    df = pd.read_csv(target_file)
    return df
