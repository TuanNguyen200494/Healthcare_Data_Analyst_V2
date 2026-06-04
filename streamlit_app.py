import streamlit as st

general_page = st.Page(
    "app/pages/1_general.py",
    title = "Thông tin vận hành"
)

patient_attention = st.Page(
    "app/pages/2_patients.py",
    title= "Thông tin về bệnh nhân"
)

doctor_information = st.Page(
    "app/pages/3_doctors.py",
    title= "Thông tin về bác sĩ"
)

lab_information = st.Page(
    "app/pages/4_labs.py",
    title = "Phòng Lab"
)

configuration = st.Page(
    "app/pages/n_configurations.py",
    title = "Configuration"
)

nav = st.navigation(
    [
        general_page,
        patient_attention,
        doctor_information,
        lab_information,
        configuration
    ],
    position="top"
)

nav.run()