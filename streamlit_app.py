import streamlit as st

general_page = st.Page(
    "app/pages/1_general.py",
    title = "Thông tin vận hành"
)

patient_attention = st.Page(
    "app/pages/2_patients.py",
    title= "Thông tin về bệnh nhân"
)

configuration = st.Page(
    "app/pages/n_configurations.py",
    title = "Configuration"
)

nav = st.navigation(
    [
        general_page,
        patient_attention,
        configuration
    ],
    position="top"
)

nav.run()