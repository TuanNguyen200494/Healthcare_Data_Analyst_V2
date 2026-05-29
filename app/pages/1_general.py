import streamlit as st
import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from app.services.load_data import load_data
from app.config.paths import find_root_project
from app.config.configs import get_raw_data_configures
from app.services.validate_columns import sum_validate
from app.services.random_remaining_cost_billing import actual_payment



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

required_tables = ['Patients', 'Encounters', 'Admissions', 'Beds', 'Critical_Lists', 'Billing', 'Departments']

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

    billing_df_filename = configureraw[configureraw["table"]=="Billing"]["file"].values[0]
    billing_df_data = load_data(billing_df_filename)
    billing_df_data_added = billing_df_data
    #billing_df_data_added['patient_payable'] = pd.to_numeric(billing_df_data_added['patient_payable'])
    billing_df_data_added['actual_payment'] = billing_df_data_added.apply(actual_payment, axis=1)
    #billing_df_data_added['total_charge'] = pd.to_numeric(billing_df_data_added['total_charge'])
    billing_df_data_added['bill_date'] = pd.to_datetime(billing_df_data_added['bill_date'])
    billing_df_data_added['billing_year'] = billing_df_data_added['bill_date'].dt.year
    billing_df_data_added['billing_month'] = billing_df_data_added['bill_date'].dt.month

    department_df_filename = configureraw[configureraw["table"]=="Departments"]["file"].values[0]
    department_df_data = load_data(department_df_filename)
    list_dept = department_df_data['department_id'].tolist()

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
    with st.container(border=True):
        st.write("Thông tin Doanh Thu")
        #st.dataframe(billing_df_data_added)

        col1 , col2 ,col3 = st.columns(3)

        with col1:
            value = round(billing_df_data_added['total_charge'].sum(),2)
            st.metric(label="Tổng Viện Phí(USD)", value = value, border = True)
        with col2:
            value_1 = round(billing_df_data_added['actual_payment'].sum()+billing_df_data_added['insurance_covered'].sum(),2)
            st.metric(label="Thực Nhận(USD)", value = value_1, border = True)
        with col3:
            value_2 = round(value - value_1,2)
            st.metric(label="Nợ Phí(USD)", value = value_2, border = True)

        if 'select_year' not in st.session_state:
                st.session_state.select_year = None
        
        list_year = billing_df_data_added['billing_year'].unique().tolist()
        index = 0

        if (st.session_state.select_year in list_year):
            index = list_year.index(st.session_state.select_year)

        billing_by_year = billing_df_data_added.groupby('billing_year').agg(
            {
                'service_charge': 'sum',
                'medication_charge': 'sum',
                'lab_charge': 'sum',
                'room_charge': 'sum',
                'total_charge': 'sum',
                'insurance_covered': 'sum',
                'patient_payable': 'sum',
                'actual_payment': 'sum'
            }
        ).reset_index()
        billing_by_year['debit_charge'] = billing_by_year['patient_payable'] - billing_by_year['actual_payment']
        #st.dataframe(billing_by_year)

        fig, ax = plt.subplots(figsize=(20,15))

        bar1 = ax.bar(
            billing_by_year['billing_year'],
            billing_by_year['service_charge'],
            label = "Service Charge",
            color = "blue",
        )
        ax.bar_label(bar1, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

        bar2 = ax.bar(
            billing_by_year['billing_year'],
            billing_by_year['medication_charge'],
            bottom=billing_by_year['service_charge'],
            label = "Medication Charge",
            color = "green",
        )
        ax.bar_label(bar2, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

        bar3 = ax.bar(
            billing_by_year['billing_year'],
            billing_by_year['lab_charge'],
            bottom=(billing_by_year['service_charge'] + billing_by_year['medication_charge']),
            label = "Lab Charge",
            color = "yellow",
        )
        ax.bar_label(bar3, fmt="{:,.2f}", label_type="center", color="red", fontweight="bold")

        bar4 = ax.bar(
            billing_by_year['billing_year'],
            billing_by_year['room_charge'],
            bottom=(billing_by_year['service_charge'] + billing_by_year['medication_charge']+billing_by_year['lab_charge']),
            label = "Room Charge",
            color = "red",
        )
        ax.bar_label(bar4, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

        ax.plot(
            billing_by_year['billing_year'],
            billing_by_year['debit_charge'],
            label = "Nợ Phí",
            color = "gray",
            linewidth=3,
            marker = 'o',
            markersize = 8,
        )

        ax.set_xlabel("Năm")
        ax.set_ylabel("Số Tiền")
        ax.legend(loc="upper right")
        with st.expander("Biểu đồ Doanh Thu, Nợ Phí qua các năm", expanded=False):
            st.pyplot(fig)
        
        st.session_state.select_year = st.selectbox("Xem Thông Tin Chi Tiết",list_year, index=index)
        df_year_selection = billing_df_data_added[billing_df_data_added['billing_year']==st.session_state.select_year]
        with st.expander(f"Biểu đồ Doanh Thu Chi Tiết Theo Tháng Trong Năm {st.session_state.select_year}",expanded=False):
            df_year_selection = df_year_selection.groupby('billing_month').agg(
                {
                    'service_charge': 'sum',
                    'medication_charge': 'sum',
                    'lab_charge': 'sum',
                    'room_charge': 'sum',
                    'total_charge': 'sum',
                    'insurance_covered': 'sum',
                    'patient_payable': 'sum',
                    'actual_payment': 'sum'
                }
            ).reset_index()
            df_year_selection['debit_charge'] = df_year_selection['patient_payable'] - df_year_selection['actual_payment']

            for c in range(1,13):
                if c not in df_year_selection['billing_month']:
                    add_row = {
                        'billing_month': c,
                        'service_charge': 0,
                        'medication_charge':0,
                        'lab_charge':0,
                        'room_charge':0,
                        'total_charge':0,
                        'insurance_covered':0,
                        'patient_payable':0,
                        'actual_payment':0,
                        'debit_charge':0
                    }
                    df_year_selection = pd.concat([df_year_selection, pd.DataFrame([add_row])])
            #st.dataframe(df_year_selection)
            fig1, ax1 = plt.subplots(figsize=(20,10))

            bar1 = ax1.bar(
            df_year_selection['billing_month'],
            df_year_selection['service_charge'],
            label = "Service Charge",
            color = "blue",
            )
            ax1.bar_label(bar1, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

            bar2 = ax1.bar(
                df_year_selection['billing_month'],
                df_year_selection['medication_charge'],
                bottom=df_year_selection['service_charge'],
                label = "Medication Charge",
                color = "green",
            )
            ax1.bar_label(bar2, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

            bar3 = ax1.bar(
                df_year_selection['billing_month'],
                df_year_selection['lab_charge'],
                bottom=(df_year_selection['service_charge']+df_year_selection['medication_charge']),
                label = "Lab Charge",
                color = "yellow",
            )
            ax1.bar_label(bar3, fmt="{:,.2f}", label_type="center", color="red", fontweight="bold")

            bar4 = ax1.bar(
                df_year_selection['billing_month'],
                df_year_selection['room_charge'],
                bottom=(df_year_selection['service_charge']+df_year_selection['medication_charge']+df_year_selection['lab_charge']),
                label = "Room Charge",
                color = "red",
            )
            ax1.bar_label(bar4, fmt="{:,.2f}", label_type="center", color="white", fontweight="bold")

            ax1.plot(
                df_year_selection['billing_month'],
                df_year_selection['debit_charge'],
                label = "Nợ Phí",
                color = "gray",
                linewidth=3,
                marker = 'o',
                markersize = 8,
            )

            ax1.set_xlabel("Tháng")
            ax1.set_ylabel("Số Tiền")
            ax1.legend(loc="upper right")
            st.pyplot(fig1)
        
        with st.expander(f"Biểu Đồ Doanh Thu Chi Tiết Theo Phòng Ban Trong Năm {st.session_state.select_year}",expanded=False):
            #Dựa vào billing, encounters và departments để tạo nên DataFrame sử dụng cho dạng dữ liệu này
            ## sử dụng biểu đồ cột ngang
            df_merge = encounter_df_data.merge(billing_df_data_added, on='encounter_id', how='inner')[['encounter_id','department_id','doctor_id','chief_complaint', 'diagnosis_code', 'severity_level', 'service_charge', 'medication_charge', 'lab_charge', 'room_charge','total_charge','insurance_covered','patient_payable','payment_status','actual_payment', 'billing_year','billing_month']]
            df_merge = df_merge.merge(department_df_data, on='department_id', how='inner')
            #st.dataframe(df_merge)
            df_year_selection_dept_detail = df_merge[df_merge['billing_year']==st.session_state.select_year]
            #st.dataframe(df_year_selection_dept_detail)
            df_year_selection_dept_detail = df_year_selection_dept_detail.groupby('department_id').agg(
                {
                    'service_charge':'sum',
                    'medication_charge':'sum',
                    'lab_charge':'sum',
                    'room_charge':'sum',
                    'total_charge': 'sum',
                    'insurance_covered': 'sum',
                    'patient_payable': 'sum',
                    'actual_payment':'sum'
                }
            ).reset_index()
            for dept in list_dept:
                if dept not in df_year_selection_dept_detail['department_id'].tolist():
                    add_zero = {
                        'department_id': dept,
                        'service_charge':0,
                        'medication_charge':0,
                        'lab_charge':0,
                        'room_charge':0,
                        'total_charge':0,
                        'insurance_covered': 0,
                        'patient_payable':0,
                        'actual_payment':0                       
                    }
                    df_year_selection_dept_detail = pd.concat([df_year_selection_dept_detail, pd.DataFrame([add_zero])])
            df_year_selection_dept_detail['debit_charge'] = df_year_selection_dept_detail['patient_payable'] - df_year_selection_dept_detail['actual_payment']
            df_year_selection_dept_detail = df_year_selection_dept_detail.sort_values(by=['total_charge'])
            #st.dataframe(df_year_selection_dept_detail)

            fig2, ax2 = plt.subplots(figsize=(15,12))
            bar1_1 = ax2.barh(
                df_year_selection_dept_detail['department_id'],
                df_year_selection_dept_detail['insurance_covered'],
                label = "Insurance",
                color = 'blue'
            )
            bar2_2 = ax2.barh(
                df_year_selection_dept_detail['department_id'],
                df_year_selection_dept_detail['actual_payment'],
                left = df_year_selection_dept_detail['insurance_covered'],
                label = "Service Charge",
                color = 'green'
            )
            bar3_3 = ax2.barh(
                df_year_selection_dept_detail['department_id'],
                df_year_selection_dept_detail['debit_charge'],
                left = df_year_selection_dept_detail['insurance_covered']+df_year_selection_dept_detail['actual_payment'],
                label = "Debit Charge",
                color = 'red'
            )

            ax2.set_xlabel("Số Tiền")
            ax2.set_ylabel("Phòng Ban")
            ax2.legend(loc="upper right")
            st.pyplot(fig2)