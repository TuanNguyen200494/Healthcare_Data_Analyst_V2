import streamlit as st
import pandas as pd
from datetime import datetime,timedelta

from app.services.load_data import load_data
from app.config.paths import find_root_project

from app.services.validate_columns import sum_validate

from app.config.configs import get_raw_data_configures

from app.services.import_new_appointment import import_new_appointment

st.set_page_config(
    page_title="Phòng Lab",
    layout = "wide"
)

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

configureraw = get_raw_data_configures(full_path)

required_tables = ['LabResults','LabOrders','Encounters','Patients', 'Doctors', 'Departments', 'Appointments']

result = sum_validate(required_tables)
if (result):
    st.success("các feature dữ liệu yêu cầu thoả điều kiện")
else:
    st.error("Một trong các dữ liệu đã sai")


if (result):
    laborder_df_filename = configureraw[configureraw["table"]=="LabOrders"]["file"].values[0]
    laborder_df_data = load_data(laborder_df_filename)

    labresult_df_filename = configureraw[configureraw["table"]=="LabResults"]["file"].values[0]
    labresult_df_data = load_data(labresult_df_filename)

    encounter_df_filename = configureraw[configureraw["table"]=="Encounters"]["file"].values[0]
    encounter_df_data = load_data(encounter_df_filename)

    encounter_df_data["encounter_date"] = pd.to_datetime(encounter_df_data["encounter_date"])
    encounter_df_data["encounter_year"] = encounter_df_data["encounter_date"].dt.year
    encounter_df_data["encounter_month"] = encounter_df_data["encounter_date"].dt.month

    patient_df_filename = configureraw[configureraw["table"]=="Patients"]["file"].values[0]
    patient_df_data = load_data(patient_df_filename)

    doctor_df_filename = configureraw[configureraw["table"]=="Doctors"]["file"].values[0]
    doctor_df_data = load_data(doctor_df_filename)

    department_df_filename = configureraw[configureraw["table"]=="Departments"]["file"].values[0]
    department_df_data = load_data(department_df_filename)

    appointment_df_filename = configureraw[configureraw["table"]=="Appointments"]["file"].values[0]
    appointment_df_data = load_data(appointment_df_filename)
    appointment_df_data['appointment_date'] = pd.to_datetime(appointment_df_data['appointment_date'],format="%Y-%m-%d")

    def get_doctor_name(doctor_id):
        return doctor_df_data[doctor_df_data['doctor_id']== doctor_id]['doctor_name'].values[0]
    
    def get_department_name(department_id):
        return department_df_data[department_df_data['department_id']== department_id]['department_name'].values[0]



if (result):
    ## Tính số xét nghiệm đang đợi

    ##Cảnh báo số xét nghiệm có flag = true, của các bệnh nhân mà ngày trả kết quả lớn hơn ngày encounter gần nhất của bệnh nhân.
    df_high_lab_result = labresult_df_data[labresult_df_data['result_flag']=="High"]
    #st.dataframe(df_high_lab_result)
    latest_encounter = encounter_df_data.sort_values("encounter_date", ascending = False)
    #st.dataframe(latest_encounter)
    latest_encounter = latest_encounter.drop_duplicates(subset=["patient_id"], keep = "first")
    #st.dataframe(latest_encounter)
    merge_df = df_high_lab_result.merge(latest_encounter,on="patient_id", how="inner")
    #st.dataframe(merge_df)
    result_df = merge_df[merge_df["encounter_date"] < merge_df["resulted_at"]]
    #st.dataframe(result_df)
    #st.metric(label="Số xét nghiệm cao, cần cảnh giác", value = result_df['lab_order_id'].count(), border=True)
    col1,col2 = st.columns(2)
    with col1:
        st.metric(label="Số Lượng xét nghiệm đang đợi", value = laborder_df_data[laborder_df_data["result_status"]== "Pending"]['lab_order_id'].count(), border=True)
    with col2:
        st.metric(label="Số xét nghiệm cao, cần cảnh giác", value = result_df['lab_order_id'].count(), border=True)
    
    selected_test_name = st.selectbox(label = "Chuyên mục", options = result_df['test_name'].unique())

    selected_field = result_df[result_df['test_name']==selected_test_name][['patient_id','result_value', 'resulted_at', 'chief_complaint']]
    selected_field = selected_field.merge(patient_df_data, on="patient_id", how="inner")

    row = st.dataframe(selected_field[['full_name', 'age', 'blood_type', 'result_value', 'chief_complaint']],hide_index=True, selection_mode='single-row', on_select="rerun")
    selected_patient_id = None
    selected_patient_name = None

    if len(row.selection.rows) > 0:
        selected_row_index = row.selection.rows[0]
        selected_patient_id = selected_field.iloc[selected_row_index]["patient_id"]
        selected_patient_name = selected_field.iloc[selected_row_index]["full_name"]
        st.session_state.selected_patient_for_appointment = selected_patient_id

        if ('duplicate_patient_appointment_page4' not in st.session_state):
            st.session_state.duplicate_patient_appointment_page4 = False
        if ('duplicate_doctor_appointment_page4' not in st.session_state):
            st.session_state.duplicate_doctor_appointment_page4 = False
        if ('approve_scheduled_page4' not in st.session_state):
            st.session_state.approve_scheduled_page4 = False

        with st.expander(f"Tạo lịch hẹn cho {selected_patient_name}", expanded=True):
            currentdate_dt = pd.to_datetime(datetime.now(), format="%Y-%m-%d")
            df_appointment_with_select_patient = appointment_df_data[(appointment_df_data['appointment_date']>currentdate_dt) & (appointment_df_data['patient_id']==selected_patient_id)]

            date_appointments = st.date_input("Chọn Ngày Tái Khám", min_value=currentdate_dt, max_value= currentdate_dt + timedelta(days=730),key="appointment_date_page4")
            time_appointments = st.time_input("Chọn Giờ Điều Trị",key="appointment_time_page4")
            reason = st.text_input("Lý do tái khám",key="appointment_reason_page4")
            doctor_appointments = st.selectbox(label = "Chọn Bác Sĩ Điều trị", options=doctor_df_data['doctor_id'], format_func=get_doctor_name,key="appointment_doctor_page4")
            department_appointments = st.selectbox(label = "Khoa Điều Trị", options=department_df_data['department_id'], format_func=get_department_name,key="appointment_department_page4")
            st.session_state.duplicate_patient_appointment_page4 = False
            st.session_state.duplicate_doctor_appointment_page4 = False
            st.session_state.approve_scheduled_page4 = False

            for index, row in df_appointment_with_select_patient.iterrows():
                if(date_appointments.strftime('%Y-%m-%d') == row['appointment_date'].strftime('%Y-%m-%d') and time_appointments.strftime('%H:%M') == row['appointment_time']):
                    st.session_state.duplicate_patient_appointment_page4 = True
                    break 

            df_get_list_appointment_of_doctor = appointment_df_data[(appointment_df_data['doctor_id']==doctor_appointments)]
            for index, row in df_get_list_appointment_of_doctor.iterrows():
                if(date_appointments.strftime('%Y-%m-%d') == row['appointment_date'].strftime('%Y-%m-%d') and time_appointments.strftime('%H:%M') == row['appointment_time']):
                    st.session_state.duplicate_doctor_appointment_page4 = True
                    break

            if(st.session_state.duplicate_patient_appointment_page4):
                st.error("Đã trùng lịch của bệnh nhân - Không Thể Tạo Lịch Hẹn")
                st.session_state.approve_scheduled_page4 = False
            elif(st.session_state.duplicate_doctor_appointment_page4):
                st.error("Trùng Lịch với bác sĩ - Không Thể Tạo Lịch Hẹn")
                st.session_state.approve_scheduled_page4 = False
            else:
                st.success("Có thể tạo Lịch Tái Khám")
                st.session_state.approve_scheduled_page4 = True 

            if st.button("Tạo lịch hẹn") and (st.session_state.approve_scheduled_page4):
                row_collected = {
                    "patient_id": selected_patient_id,
                    "doctor_id": doctor_appointments,
                    "department_id": department_appointments,
                    "appointment_date": date_appointments.strftime("%Y-%m-%d"),
                    "appointment_time": time_appointments.strftime('%H:%M'),
                    "appointment_status": "Scheduled",
                    "reason_for_visit": reason,
                    "created_at": datetime.now().strftime('%Y-%m-%d')
                }
                migrate_df = import_new_appointment(appointment_df_data,pd.DataFrame([row_collected]))

                migrate_df["appointment_date"] = pd.to_datetime(
                    migrate_df["appointment_date"]
                ).dt.strftime("%Y-%m-%d")

                full_path_appointment = root / "data" / "raw" / appointment_df_filename
                migrate_df.to_csv(full_path_appointment,index=False)

                st.cache_data.clear()
                st.session_state.approve_scheduled_page4 = False
                st.rerun()


