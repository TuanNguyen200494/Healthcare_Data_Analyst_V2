#### sử dụng để cho table billing.csv, dùng cho các bill ở trạng phái pending, hoặc partially paid -> random ra số tiền đã trả
import pandas as pd
import random

def actual_payment(row):
    payment_status = row['payment_status']
    patient_payable = row['patient_payable']
    if payment_status == "Paid":
        return patient_payable
    elif payment_status == "Pending" or payment_status == "Denied":
        return 0
    elif payment_status == "Partially Paid":
        return patient_payable * round(random.uniform(0.1, 0.8),2)
    else:
       return 0


