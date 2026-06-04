import streamlit as st
import pandas as pd
from datetime import datetime,timedelta

from app.services.load_data import load_data
from app.config.paths import find_root_project

from app.services.validate_columns import sum_validate

from app.config.configs import get_raw_data_configures

st.set_page_config(
    page_title="Phòng Lab",
    layout = "wide"
)

root = find_root_project()
json_config_name = "rawdata_config.json"

full_path = root / "app" / "config" / json_config_name

configureraw = get_raw_data_configures(full_path)

required_tables = ['LabResults','LabOrders','Encounters','Patients']

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

        with st.expander(f"Tạo lịch hẹn cho {selected_patient_name}", expanded=True):
            appointment_date = st.date_input("Chọn ngày tái khám")
            appointment_time = st.time_input("Chọn giờ tái khám")
            reason = st.text_input("Lý do tái khám")

            if st.button("Tạo lịch hẹn"):
                pass

