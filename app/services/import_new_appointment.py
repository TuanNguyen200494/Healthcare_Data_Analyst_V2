import pandas as pd


def import_new_appointment(df:pd.DataFrame, row:pd.DataFrame):
    last_id = df.iloc[-1]['appointment_id']
    number = last_id.replace("APT","")
    next_id = int(number)+1

    new_id = "APT"+str(next_id).zfill(8)

    row["appointment_id"] = new_id

    df = pd.concat([df, row])

    return df