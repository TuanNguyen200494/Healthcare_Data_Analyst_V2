import streamlit as st
import json
import pandas as pd
from datetime import datetime

from app.services.load_data import load_data
from app.config.paths import find_root_project

from app.config.configs import get_raw_data_configures

from app.services.validate_columns import sum_validate

st.set_page_config(
    page_title="Thông tin bệnh nhân",
    layout = "wide"
)

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

#df_root_patient = load_data("patients.csv")

## Tìm vào file config rawdata"
configureraw = get_raw_data_configures(full_path)

required_tables = ['Patients', 'Critical_Lists', 'Encounters', 'Departments', 'Doctors', 'Diagnoses' 'LabOrders', 'LabResults', 'Medications', 'Prescriptions']

result = sum_validate(required_tables)
if (result):
    st.success("các feature dữ liệu yêu cầu thoả điều kiện")
else:
    st.error("Một trong các dữ liệu đã sai")

if(result):
    patient_df_filename = configureraw[configureraw["table"]=="Patients"]["file"].values[0]
    patient_df_data = load_data(patient_df_filename)

    patient_df_data["registration_date"] = pd.to_datetime(patient_df_data["registration_date"])
    patient_df_data["registration_year"] = patient_df_data["registration_date"].dt.year
    patient_df_data["registration_month"] = patient_df_data["registration_date"].dt.month

    critical_list_df_filename = configureraw[configureraw["table"]=="Critical_Lists"]["file"].values[0]
    critical_list_df_data = load_data(critical_list_df_filename)

    encounter_df_filename = configureraw[configureraw["table"]=="Encounters"]["file"].values[0]
    encounter_df_data = load_data(encounter_df_filename)

    encounter_df_data["encounter_date"] = pd.to_datetime(encounter_df_data["encounter_date"])
    encounter_df_data["encounter_year"] = encounter_df_data["encounter_date"].dt.year
    encounter_df_data["encounter_month"] = encounter_df_data["encounter_date"].dt.month

    department_df_filename = configureraw[configureraw["table"]=="Departments"]["file"].values[0]
    department_df_data = load_data(department_df_filename)

    doctor_df_filename = configureraw[configureraw["table"]=="Doctors"]["file"].values[0]
    doctor_df_data = load_data(doctor_df_filename)

    diagnose_df_filename = configureraw[configureraw["table"]=="Diagnoses"]["file"].values[0]
    diagnose_df_data = load_data(diagnose_df_filename)

    laborder_df_filename = configureraw[configureraw["table"]=="LabOrders"]["file"].values[0]
    laborder_df_data = load_data(laborder_df_filename)

    labresult_df_filename = configureraw[configureraw["table"]=="LabResults"]["file"].values[0]
    labresult_df_data = load_data(labresult_df_filename)

    medication_df_filename = configureraw[configureraw["table"]=="Medications"]["file"].values[0]
    medication_df_data = load_data(medication_df_filename)

    prescription_df_filename = configureraw[configureraw["table"]=="Prescriptions"]["file"].values[0]
    prescription_df_data = load_data(prescription_df_filename)

    with st.container(border=True):
            st.write("Tình trạng rủi ro các ca bệnh")
            col1, col2 = st.columns(2)
            value_1 = critical_list_df_data[(critical_list_df_data['watchlist_status']!= 'Completed') & (critical_list_df_data['risk_level']=="Critical")]['watchlist_id'].count()

            with col1:
                value = critical_list_df_data[critical_list_df_data['watchlist_status']!= 'Completed']['watchlist_id'].count()
                st.metric(label = "Tổng số ca cần theo dõi", value = value, border=True)
            
            with col2:
                st.metric(label = "Số ca đặc biệt nguy hiểm", value = value_1, border=True)

            if(value_1 > 0):
                with st.container(border = True):
                    st.write("Chi tiết các ca bệnh rủi ro")
                    if 'select_patient' not in st.session_state:
                        st.session_state.select_patient = None
                    ##dựa vào danh patient_id trong high_risk_patient_watchlist, lấy thông tin readable của bệnh nhân từ patients, hiển thị tên - tuổi thay vì patients_id
                    critical_list_patient_id = critical_list_df_data[(critical_list_df_data['watchlist_status']!= 'Completed') & (critical_list_df_data['risk_level']=="Critical")]

                    #merge 2 Df
                    readable_patient_id_df = critical_list_patient_id.merge(patient_df_data,on='patient_id',how='inner')
                    #st.dataframe(readable_patient_id_df)
                    select_patient_list = (readable_patient_id_df['full_name'] + " - Age: " + readable_patient_id_df['age'].astype(str)).tolist()
                    index = 0

                    if (st.session_state.select_patient in select_patient_list):
                        index = select_patient_list.index(st.session_state.select_patient)

                    st.session_state.select_patient = st.selectbox("Chọn bệnh nhân",select_patient_list, index=index)
                    patient_information_button = st.button("Xem bệnh nhân")
                    if(patient_information_button):
                        result_personal_information_df = patient_df_data[patient_df_data['full_name'] + " - Age: " + patient_df_data['age'].astype(str) == st.session_state.select_patient]
                        select_patient_id = result_personal_information_df['patient_id'].values[0]
                        with st.container(border=True):                           
                            #st.dataframe(result_personal_information_df)
                            st.write("THÔNG TIN CÁ NHÂN")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("Họ Tên: " + result_personal_information_df['full_name'].values[0])
                                st.write("Giới Tính: " + result_personal_information_df['gender'].values[0])
                                st.write("Nhóm Máu: " + result_personal_information_df['blood_type'].values[0])
                            with col2:
                                st.write("Tuổi: " + result_personal_information_df['age'].values[0].astype(str))
                                st.write("Ngày Sinh " + result_personal_information_df['date_of_birth'].values[0])
                                st.write("Nơi Sinh " + result_personal_information_df['city'].values[0] + " - " + result_personal_information_df['district'].values[0])
                        
                        with st.container(border=True):
                            st.write("LỊCH SỬ THĂM KHÁM")
                            encounter_history_df = encounter_df_data[encounter_df_data['patient_id'] == select_patient_id]
                            encounter_history_df['encounter_date'] = pd.to_datetime(encounter_history_df['encounter_date'])
                            encounter_history_df = encounter_history_df.sort_values("encounter_date")
                            st.dataframe(encounter_history_df)
                            for index, row in encounter_history_df.iterrows():
                                with st.container(border = True):
                                    encounter_id = row['encounter_id']
                                    st.write("Ngày Khám: " + row['encounter_date'].strftime('%d-%m-%Y %H:%M:%S'))
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("Nguyên Nhân: " + row['chief_complaint'])
                                        st.write("Khoa Tiếp Nhận Yêu Cầu: " + department_df_data[department_df_data['department_id']==row['department_id']]['department_name'].values[0])
                                        st.write("Kết Luận: "+ diagnose_df_data[diagnose_df_data['diagnosis_code']==row['diagnosis_code']]['diagnosis_name'].values[0])
                                    with col2:
                                        st.write("Phương Thức Tiếp Cận: " + row['encounter_type'])
                                        st.write("Bác Sĩ Phụ Trách: " + doctor_df_data[doctor_df_data['doctor_id']==row['doctor_id']]['doctor_name'].values[0])
                                        st.write("Mức độ nghiêm trọng: " + row['severity_level'])

                                    with st.container(border=True):
                                        st.write("KẾT QUẢ XÉT NGHIỆM")
                                        ##Mergee lab order and lab results with encounter_id
                                        lab_order_with_encounterid = laborder_df_data[laborder_df_data['encounter_id']==encounter_id]
                                        #st.dataframe(lab_order_with_encounterid)
                                        merge_order_with_result = lab_order_with_encounterid.merge(labresult_df_data,on='lab_order_id',how='inner')[['test_name_x', 'ordered_at','resulted_at', 'result_value', 'normal_low', 'normal_high', 'unit']].rename(columns={
                                            'test_name_x': 'Chỉ số Kiểm Tra',
                                            'ordered_at': "Ngày Kiểm Tra",
                                            'resulted_at': "Ngày Trả Kết Quả",
                                            'result_value': 'Kết Quả',
                                            'normal_low': 'Ngưỡng Chấp Nhận Thấp',
                                            'normal_high': 'Ngưỡng Chấp Nhận Cao',
                                            'unit': 'Đơn Vị'
                                        })
                                        st.dataframe(merge_order_with_result)
                                    
                                    with st.container(border=True):
                                        st.write("THÔNG TIN ĐƠN THUỐC")
                                        prescription_with_encounterid = prescription_df_data[prescription_df_data['encounter_id']==encounter_id]
                                        merge_prescription_with_medication = prescription_with_encounterid.merge(medication_df_data, on='medication_id', how='inner')[['medication_name', 'medication_group', 'dosage', 'frequency', 'duration_days', 'unit_cost']].rename(columns={
                                            'medication_name': 'Tên Thuốc',
                                            'medication_group': 'Nhóm Thuốc',
                                            'dosage': 'Số Lượng',
                                            'frequency': "Hướng Dẫn Uống",
                                            'duration_days': 'Số Ngày Dùng Thuốc',
                                            'unit_cost': 'Đơn Giá'
                                        })
                                        st.dataframe(merge_prescription_with_medication)


                                