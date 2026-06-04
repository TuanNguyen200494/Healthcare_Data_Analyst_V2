import streamlit as st
import pandas as pd
from datetime import datetime,timedelta

from app.services.load_data import load_data
from app.config.paths import find_root_project

from app.services.validate_columns import sum_validate

from app.config.configs import get_raw_data_configures

st.set_page_config(
    page_title="Thông tin Bác Sĩ",
    layout = "wide"
)

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

configureraw = get_raw_data_configures(full_path)

required_tables = ['Doctors', 'Departments', 'Encounters', 'Appointments', 'Patients']


result = sum_validate(required_tables)
if (result):
    st.success("các feature dữ liệu yêu cầu thoả điều kiện")
else:
    st.error("Một trong các dữ liệu đã sai")

if (result):
    encounter_df_filename = configureraw[configureraw["table"]=="Encounters"]["file"].values[0]
    encounter_df_data = load_data(encounter_df_filename)

    encounter_df_data["encounter_date"] = pd.to_datetime(encounter_df_data["encounter_date"])
    encounter_df_data["encounter_year"] = encounter_df_data["encounter_date"].dt.year
    encounter_df_data["encounter_month"] = encounter_df_data["encounter_date"].dt.month

    department_df_filename = configureraw[configureraw["table"]=="Departments"]["file"].values[0]
    department_df_data = load_data(department_df_filename)

    department_option = department_df_data['department_id'].tolist()

    if "select_department_page3" not in st.session_state:
        st.session_state.select_department_page3 = department_option[0]
    
    if st.session_state.select_department_page3 in department_option:
        dept_index = department_option.index(st.session_state.select_department_page3)
    else:
        dept_index = 0
        st.session_state.select_department_page3 = department_option[0]
        

    doctor_df_filename = configureraw[configureraw["table"]=="Doctors"]["file"].values[0]
    doctor_df_data = load_data(doctor_df_filename)

    appointment_df_filename = configureraw[configureraw["table"]=="Appointments"]["file"].values[0]
    appointment_df_data = load_data(appointment_df_filename)
    appointment_df_data['appointment_date'] = pd.to_datetime(appointment_df_data['appointment_date'],format="%Y-%m-%d")

    patient_df_filename = configureraw[configureraw["table"]=="Patients"]["file"].values[0]
    patient_df_data = load_data(patient_df_filename)

    def get_doctor_name(doctor_id):
        return doctor_df_data[doctor_df_data['doctor_id']== doctor_id]['doctor_name'].values[0]
    
    def get_department_name(department_id):
        return department_df_data[department_df_data['department_id']== department_id]['department_name'].values[0]

if (result):
    with st.container(border=True):
        st.write("Danh sách các Bác Sĩ Theo Phòng Ban")
        select_department = st.selectbox(label = "Khoa Điều Trị", options=department_df_data['department_id'], format_func=get_department_name,index = dept_index)
        st.session_state.select_department_page3 = select_department
        active_emp_doctor_df_data = doctor_df_data[(doctor_df_data["employment_status"]=="Active")& (doctor_df_data["department_id"]==st.session_state.select_department_page3)][['doctor_id', 'doctor_name', 'gender', 'years_experience']]
        #st.dataframe(active_emp_doctor_df_data)
        count_encounter_df = encounter_df_data.groupby(['doctor_id','severity_level'])['encounter_id'].count().reset_index()
        count_encounter_df = count_encounter_df.rename(columns={
            "encounter_id":"total_encounter"
        })

        mergedf = active_emp_doctor_df_data.merge(count_encounter_df,on='doctor_id', how='inner')

        #st.dataframe(mergedf)
        pivot_severity = mergedf.pivot_table(
            index=['doctor_id', 'doctor_name', 'gender', 'years_experience'],
            columns = 'severity_level',
            values = 'total_encounter',
            aggfunc = 'sum',
            fill_value = 0
        ).reset_index()
        #st.dataframe(pivot_severity)

        pivot_severity = pivot_severity.rename(columns={
            "Critical": "Tổng ca Nguy Kịch",
            "High": "Tổng ca ưu tiên cao",
            "Moderate": "Tổng ca Ưu tiên trung bình",
            "Low": "Tổng cả Ưu tiên thấp"
        })
        with st.expander(f"Bảng Thống Kê Số lượng ca xử lý của khoa {get_department_name(st.session_state.select_department_page3)} tính tới năm {datetime.now().strftime('%Y')}",expanded = True):
            st.dataframe(pivot_severity,hide_index=True)
        with st.expander(f"Lịch Tái Khám của Khoa {get_department_name(st.session_state.select_department_page3)}",expanded=True):
            appointment_filter = appointment_df_data[appointment_df_data['appointment_date']>pd.to_datetime(datetime.now(), format="%Y-%m-%d")]
            merge_appointment_doctor_df = appointment_filter.merge(active_emp_doctor_df_data, on='doctor_id', how='inner')
            #st.dataframe(appointment_filter)
            #st.dataframe(merge_appointment_doctor_df)
            st.write("Xem Lịch Hẹn chi tiết của bác sĩ")
            with st.container(border=True):   
                #state_button_doctor_selection
                if "selection_doctor_id" not in st.session_state:
                    st.session_state.selection_doctor_id = None

                list_doctor = merge_appointment_doctor_df['doctor_id'].unique().tolist()
                cols = st.columns(len(list_doctor))                   
                for l,col in zip(list_doctor,cols):
                    with col:                   
                        if(st.button(get_doctor_name(l), key = f"button_{l}")):
                            st.session_state.selection_doctor_id = l                
                get_doctor_id = st.session_state.selection_doctor_id
                if get_doctor_id is not None:
                    df_specific_doctor = merge_appointment_doctor_df[merge_appointment_doctor_df['doctor_id'] == st.session_state.selection_doctor_id]
                    df_specific_doctor['appointment_date'] = pd.to_datetime(df_specific_doctor['appointment_date'],format="%Y-%m-%d").dt.strftime("%Y-%m-%d")
                    #st.dataframe(df_specific_doctor)
                    for index, row in df_specific_doctor.iterrows():
                        appoint_id = row['appointment_id']
                        patiend_id = row['patient_id']
                        appoint_date = row['appointment_date']
                        appoint_time = row['appointment_time']
                        reason = row['reason_for_visit']
                        date_time = appoint_date + " - " + appoint_time
                        with st.container(border=True):
                            st.write(f"Mã Tái Khám: {appoint_id}")
                            col1, col2 = st.columns(2)
                            with col1:                           
                                st.write(f"Tên Bệnh Nhân: {patient_df_data[patient_df_data['patient_id']==patiend_id]['full_name'].values[0]}")
                                st.write(f"Tuổi: {patient_df_data[patient_df_data['patient_id']==patiend_id]['age'].values[0]}")
                            with col2:
                                st.write(f"Ngày Tái Khám: {date_time}")
                                st.write(f"Mục Đích Tái Khám: {reason}")

                



