import streamlit as st
from pathlib import Path
import json


from app.ui.configure_page_sidebar import render_sidebar_configure_page
from app.config.paths import find_root_project
from app.config.configs import get_raw_data_configures


def configure_session_state():
    if ("get_raw_data_configure") not in st.session_state:
        root = find_root_project()
        full_path = root / "app" / "config" / "rawdata_config.json"
        st.session_state["get_raw_data_configure"] = get_raw_data_configures(full_path)



def get_list_raw_data():
    list_csv = []
    root = find_root_project()
    raw_dir = root / "data" / "raw"
    list_csv = sorted([
        file.name
        for file in raw_dir.glob("*.csv")
        if file.is_file()
    ])
    return list_csv

def render_for_rawdataconfig():
    st.title("Chọn dữ liệu cho các Data được yêu cầu")
    raw_data_config = st.session_state["get_raw_data_configure"]

    edited_df = st.data_editor(
        raw_data_config,
        column_config={
            "file": st.column_config.SelectboxColumn(
                "File Name",
                options=get_list_raw_data(),
                required= True
            )
        },
        disabled = ["table", "Description", "required"]
    )
    if st.button("Save configure"):
        try:
            updated_configure = edited_df.to_dict(orient = "records")
            root = find_root_project()
            configure_path = root / "app" / "config" / "rawdata_config.json"
            with open(configure_path, "w", encoding = "utf-8") as f:
                json.dump(updated_configure, f, ensure_ascii=False, indent=4)
            
            st.session_state["get_raw_data_configure"] = edited_df
            st.success("Dữ liệu configure đã được cập nhật")
        except Exception as e:
            st.error(f"có lỗi xảy ra trong quá trình udpate configure: {e}")


