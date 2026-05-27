import streamlit as st
import json
import pandas as pd
from datetime import datetime

from app.services.load_data import load_data
from app.config.paths import find_root_project

from app.config.configs import get_raw_data_configures

from app.services.validate_columns import sum_validate

st.set_page_config(
    page_title="Thông tin vận hành",
    layout = "wide"
)

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

#df_root_patient = load_data("patients.csv")

## Tìm vào file config rawdata"
configureraw = get_raw_data_configures(full_path)

required_tables = ['Patients', 'Encounters', 'Admissions', 'Beds', 'Critical_Lists']

result = sum_validate(required_tables)
if (result):
    st.success("các feature dữ liệu yêu cầu thoả điều kiện")
else:
    st.error("Một trong các dữ liệu đã sai")

## Lưu trữ đữ liệu:
if (result):
    patient_df_filename = configureraw[configureraw["table"]=="Patients"]["file"].values[0]
    patient_df_data = load_data(patient_df_filename)

    patient_df_data["registration_date"] = pd.to_datetime(patient_df_data["registration_date"])
    patient_df_data["registration_year"] = patient_df_data["registration_date"].dt.year
    patient_df_data["registration_month"] = patient_df_data["registration_date"].dt.month

    encounter_df_filename = configureraw[configureraw["table"]=="Encounters"]["file"].values[0]
    encounter_df_data = load_data(encounter_df_filename)

    encounter_df_data["encounter_date"] = pd.to_datetime(encounter_df_data["encounter_date"])
    encounter_df_data["encounter_year"] = encounter_df_data["encounter_date"].dt.year
    encounter_df_data["encounter_month"] = encounter_df_data["encounter_date"].dt.month

    admission_df_filename = configureraw[configureraw["table"]=="Admissions"]["file"].values[0]
    admission_df_data = load_data(admission_df_filename)

    admission_df_data["admission_date"] = pd.to_datetime(admission_df_data["admission_date"])
    admission_df_data["admission_year"] = admission_df_data["admission_date"].dt.year
    admission_df_data["admission_month"] = admission_df_data["admission_date"].dt.month

    bed_df_filename = configureraw[configureraw["table"]=="Beds"]["file"].values[0]
    bed_df_data = load_data(bed_df_filename)

    critical_list_df_filename = configureraw[configureraw["table"]=="Critical_Lists"]["file"].values[0]
    critical_list_df_data = load_data(critical_list_df_filename)

if(result):
# Nhóm Thông tin tổng quát về bệnh nhân
    with st.container(border=True):
        st.write(f"Thông tin về bệnh nhân, tổng số lượng: {patient_df_data["patient_id"].count()}")
        col1, col2, col3 = st.columns(3)
        with col1 :
            encounter_df_data_group = encounter_df_data.groupby(['encounter_year', 'encounter_month'])['encounter_id'].count().reset_index()
            encounter_df_data_group = encounter_df_data_group.sort_values(by = ['encounter_year',  'encounter_month'], ascending = False)
            current_value = encounter_df_data_group['encounter_id'].iloc[0]
            delta_value = str(encounter_df_data_group['encounter_id'].iloc[0] - encounter_df_data_group['encounter_id'].iloc[1]) + " so với tháng " + str(encounter_df_data_group['encounter_month'].iloc[1])
            st.metric(label = "Lượt thăm khám theo tháng:", value = current_value, delta = delta_value, border=True)

            encounter_df_data_emergency = encounter_df_data[encounter_df_data["encounter_type"]=="Emergency"]
            encounter_df_data_emergency = encounter_df_data_emergency.groupby(['encounter_year', 'encounter_month'])['encounter_id'].count().reset_index()
            encounter_df_data_emergency = encounter_df_data_emergency.sort_values(by = ['encounter_year',  'encounter_month'], ascending = False)
            current_value = encounter_df_data_emergency['encounter_id'].iloc[0]
            delta_value = str(encounter_df_data_emergency['encounter_id'].iloc[0] - encounter_df_data_emergency['encounter_id'].iloc[1]) + " so với tháng " + str(encounter_df_data_emergency['encounter_month'].iloc[1])
            st.metric(label = "Lượt cấp cứu theo tháng:", value = current_value, delta = delta_value, border=True)

        with col2 :
            patient_df_data_group = patient_df_data.groupby(['registration_year','registration_month'])['patient_id'].count().reset_index()
            patient_df_data_group = patient_df_data_group.sort_values(by = ['registration_year','registration_month'], ascending=False)
            current_value = patient_df_data_group['patient_id'].iloc[0]
            delta_value = str(patient_df_data_group['patient_id'].iloc[0] - patient_df_data_group['patient_id'].iloc[1]) + " so với tháng " + str(patient_df_data_group['registration_month'].iloc[1])
            st.metric(label ="Lượng bệnh nhân mới so với tháng trước", value = current_value,delta = delta_value, border=True)

            encounter_df_data_outpatient = encounter_df_data[(encounter_df_data["encounter_type"]=="Outpatient") | (encounter_df_data["encounter_type"]=="Follow-up")]
            encounter_df_data_outpatient = encounter_df_data_outpatient.groupby(['encounter_year', 'encounter_month'])['encounter_id'].count().reset_index()
            encounter_df_data_outpatient = encounter_df_data_outpatient.sort_values(by = ['encounter_year',  'encounter_month'], ascending = False)
            current_value = encounter_df_data_outpatient['encounter_id'].iloc[0]
            delta_value = str(encounter_df_data_outpatient['encounter_id'].iloc[0] - encounter_df_data_outpatient['encounter_id'].iloc[1]) + " so với tháng " + str(encounter_df_data_outpatient['encounter_month'].iloc[1])
            st.metric(label = "Lượt khám ngoại trú theo tháng:", value = current_value, delta = delta_value, border=True)

        with col3:
            patient_df_data_group_2 = patient_df_data.groupby('registration_year')['age'].mean().reset_index()
            patient_df_data_group_2 = patient_df_data_group_2.sort_values(by = 'registration_year', ascending = False)
            current_value = round(patient_df_data_group_2['age'].iloc[0],2)
            delta_value = str(round(patient_df_data_group_2['age'].iloc[0] - patient_df_data_group_2['age'].iloc[1],2)) + " so với năm " +str(patient_df_data_group_2['registration_year'].iloc[1])
            st.metric(label ="Độ tuổi trung bình theo năm", value = current_value,delta = delta_value, border=True)

            
            encounter_df_data_inpatient = admission_df_data.groupby(['admission_year', 'admission_month'])['admission_id'].count().reset_index()
            encounter_df_data_inpatient = encounter_df_data_inpatient.sort_values(by = ['admission_year',  'admission_month'], ascending = False)
            current_value = encounter_df_data_inpatient['admission_id'].iloc[0]
            delta_value = str(encounter_df_data_inpatient['admission_id'].iloc[0] - encounter_df_data_inpatient['admission_id'].iloc[1]) + " so với tháng " + str(encounter_df_data_inpatient['admission_month'].iloc[1])
            st.metric(label = "Lượt điều trị nội trú theo tháng:", value = current_value, delta = delta_value, border=True)
# Nhóm thông tin vận hành ở trạng thái hiện tại
    with st.container(border=True):
        st.write("Tình Trạng Vận hành hiện tại")
        col1, col2, col3 = st.columns(3)
        with col1: 
            current_value = admission_df_data[admission_df_data["discharge_date"].isna()]["admission_id"].count()
            st.metric(label ="Số bệnh nhân nội trú hiện tại", value = current_value, border = True)

            bed_avail = bed_df_data[bed_df_data["bed_status"]=="Available"]["bed_id"].count()
            st.metric(label ="Số giường trống", value = bed_avail, border = True)
        
        with col2:
            bed_occu = bed_df_data[bed_df_data["bed_status"]=="Occupied"]["bed_id"].count()
            st.metric(label ="Số giường đang sử dụng", value = bed_occu, border = True)

            bed_occu_percentage = str(round((bed_df_data[bed_df_data["bed_status"]=="Occupied"]["bed_id"].count() / bed_df_data["bed_id"].count())*100,2))+"%"
            st.metric(label = "Tỷ lệ sử dụng giường", value = bed_occu_percentage, border=True)

        with col3: 
            icu_bed_total = bed_df_data[bed_df_data["ward"].str.startswith("ICU", na=False)]["bed_id"].count()
            icu_bed_avail = bed_df_data[(bed_df_data["ward"].str.startswith("ICU", na=False)) & (bed_df_data["bed_status"]=="Available")]["bed_id"].count()
            delta = str(round((icu_bed_avail / icu_bed_total)*100,2)) +"%" + " giường trống"
            st.metric(label = "Số giường ICU trống", value = icu_bed_avail, delta = delta, border=True)

            avg_stay_date = str(round(admission_df_data["length_of_stay"].mean(),2)) + " Ngày"
            st.metric(label = "Trung bình thời gian nằm viện", value = avg_stay_date, border=True)

#Nhóm thông tin về doanh thu, bảo hiểm, công nợ