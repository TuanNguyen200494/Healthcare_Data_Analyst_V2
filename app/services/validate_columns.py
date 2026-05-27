import pandas as pd
from typing import List

from app.config.paths import find_root_project
from app.services.load_data import load_data
from app.config.configs import get_raw_data_configures

def patiens_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "patients.csv"
    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def encounters_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "encounters.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def admissions_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "admissions.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False

def beds_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "beds.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def critical_list_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "high_risk_patient_watchlist.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def department_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "departments.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False

def doctor_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "doctors.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def diagnoses_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "diagnoses.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def laborder_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "lab_orders.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def labresults_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "lab_results.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def medications_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "medications.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def prescriptions_data_validates(df: pd.DataFrame)->bool:
    root = find_root_project()
    data = "prescriptions.csv"

    full_path = root / "data" / "raw" / data
    org_df = pd.read_csv(full_path)
    list_columns = org_df.columns.to_list()

    df_column = df.columns.to_list()

    if (set(list_columns) == set(df_column)):
        return True
    else:
        return False
    
def sum_validate(list_table:List):
    root = find_root_project()
    json_config_name = "rawdata_config.json"
    full_json_path = root / "app" / "config" / json_config_name
    configureraw = get_raw_data_configures(full_json_path)
    for l in list_table:
        table_need_to_check = configureraw[configureraw["table"]==l]
        if (l =="Patients"):
            result = patiens_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Encounters"):
            result = encounters_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Admissions"):
            result = admissions_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Beds"):
            result = beds_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Critical_Lists"):
            result = critical_list_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Departments"):
            result = department_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Doctors"):
            result = doctor_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Diagnoses"):
            result = diagnoses_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "LapOrders"):
            result = laborder_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "LabResults"):
            result = labresults_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Medications"):
            result = medications_data_validates(load_data(table_need_to_check["file"].values[0]))
        elif(l == "Prescriptions"):
            result = prescriptions_data_validates(load_data(table_need_to_check["file"].values[0]))
        if not result:
            return result
            break
    
    return result

            