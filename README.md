# Healthcare_Data_Analyst_V2
Sử dụng Dataset lớn và đa dạng hơn, phục vụ tốt hơn cho việc phân tích sự khác biệt giữa các chỉ số sức khoẻ, điều kiện, kết quả vận hành, KPI, và tích hợp dự đoán

# Thông tin các Dataset hiện tại
## 1. patients : Thông tin bệnh nhân
patient_id
patient_code
full_name
gender
date_of_birth
age
blood_type
city
district
insurance_type
chronic_condition_flag
registration_date

## 2. departments : Các khoa khám bệnh / phòng khám bệnh: Emergency / Internal Medicine / Cardiology / Pediatrics / Orthopedics / Obstetrics / Surgery / ICU / Laboratory / Radiology / Outpatient Clinic
department_id
department_name
department_type
floor
bed_capacity

## 3. doctors: Thông tin bác sĩ:
doctor_id
doctor_name
department_id
specialty
years_experience
employment_status

## 4. appointments: Lịch hẹn khám
appointment_id
patient_id
doctor_id
department_id
appointment_date
appointment_time
appointment_status
reason_for_visit

## 5. encouters: lần đến viện của bệnh nhân
encounter_id
patient_id
encounter_type
department_id
doctor_id
encounter_date
chief_complaint
diagnosis_code
diagnosis_name
severity_level
encounter_status

## 6. admissions: Thông tin nhập viện
admission_id
patient_id
encounter_id
department_id
admission_date
discharge_date
length_of_stay
admission_type
admission_status
discharge_disposition
readmission_30d_flag

## 7. beds: giường bệnh
bed_id
department_id
ward
room
bed_number
bed_status

## 8. bed_assignments: Lịch sử bệnh nhân sử dụng giường bệnh
bed_assignment_id
admission_id
patient_id
bed_id
assigned_at
released_at
assignment_status

## 9. diagnoses: Chẩn đoán
diagnosis_code
diagnosis_name
diagnosis_group
is_chronic
risk_weight

## 10. lab_orders: Chỉ định xét nghiệm
lab_order_id
encounter_id
patient_id
doctor_id
test_name
ordered_at
result_status
priority

## 11. lab_results: kết quả xét nghiệm
lab_result_id
lab_order_id
patient_id
test_name
result_value
normal_low
normal_high
result_flag
resulted_at

## 12. medications: Doanh mục thuốc
medication_id
medication_name
medication_group
unit_cost
requires_prescription

## 13. prescriptions: Đơn thuốc
prescription_id
encounter_id
patient_id
doctor_id
medication_id
dosage
frequency
duration_days
prescribed_at

## 14. billing : viện phí
bill_id
patient_id
encounter_id
admission_id
bill_date
service_charge
medication_charge
lab_charge
room_charge
insurance_covered
patient_payable
payment_status

## 15. current_inpatients : Bệnh nhân nằm viện hiện tại
patient_id
admission_id
department_id
bed_id
admission_date
days_in_hospital
current_severity
estimated_discharge_date
care_status

## 16. patient_risk_summary: Đánh giá rủi ro của các bệnh nhân
patient_id
latest_encounter_date
age
chronic_condition_count
admission_count_12m
ed_visit_count_6m
avg_length_of_stay
abnormal_lab_count
critical_lab_count
unpaid_bill_amount
readmission_30d_flag
risk_score
risk_level




#### Automation options ###
# 1. Tự động tạo báo cáo vận hành bệnh viện
| Sheet                  | Nội dung                                                   |
| ---------------------- | ---------------------------------------------------------- |
| Executive Summary      | tổng bệnh nhân, lượt khám, nhập viện, doanh thu, occupancy |
| Department Performance | hiệu suất theo khoa                                        |
| Current Inpatients     | bệnh nhân đang nằm viện                                    |
| Bed Occupancy          | tỷ lệ sử dụng giường                                       |
| Emergency Trend        | lượt cấp cứu theo tháng                                    |
| Billing Summary        | công nợ, bảo hiểm, thanh toán                              |
| Lab Status             | xét nghiệm pending/critical                                |
| Risk Patients          | bệnh nhân nguy cơ cao                                      |


# 2. Tự động xuất danh sách bệnh nhân cần theo dõi
chọn rule :
Nếu age >= 65 và có chronic condition → risk tăng
Nếu nhập viện >= 2 lần trong 12 tháng → risk tăng
Nếu ED visit >= 3 lần trong 6 tháng → risk tăng
Nếu có critical lab result → risk tăng
Nếu vừa discharge và có readmission risk cao → cần follow-up
Nếu unpaid bill cao → financial follow-up

| Sheet                  | Nội dung                        |
| ---------------------- | ------------------------------- |
| Critical Clinical Risk | bệnh nhân nguy cơ lâm sàng cao  |
| Readmission Risk       | nguy cơ tái nhập viện           |
| Abnormal Lab Follow-up | xét nghiệm bất thường cần xử lý |
| Chronic Care Follow-up | bệnh mạn tính cần theo dõi      |
| Billing Follow-up      | công nợ cần xử lý               |


# 3. Tự động kiểm tra thông tin trước khi xuất viện
có lab result pending không?
có medication chưa kê không?
có bill chưa hoàn tất không?
có follow-up appointment chưa?
có risk cao cần care plan không?

Output :

Môt file ghi lại toàn bộ quá trình điều trị

# 4. Tự động báo cáo doanh thu và bảo hiểm
doanh thu theo khoa
doanh thu theo tháng
tỷ lệ bảo hiểm chi trả
số tiền bệnh nhân phải trả
pending payment
denied claims


###### BÀI TOÁN DỰ ĐOÁN
# 1. Danh sách có khả năng tái nhập viện trong 30 ngày : Predict 30-day readmission

