import dbconnect as db
from dbconnect import getDataFromDB, modifyDB

# Get the appointment Date and Time
sql = """
        SELECT 
            p.payment_id, 
            p.payment_status, 
            TO_CHAR(p.payment_date, 'DD, Month YYYY') AS formatted_date, 
            CONCAT(pt.patient_first_m, ' ', pt.patient_last_m) AS patient_name
        FROM Payment p
        JOIN Appointment a ON p.payment_id = a.payment_id
        JOIN Patient pt ON a.patient_id = pt.patient_id
        WHERE p.payment_id = %s AND p.payment_delete = false
    """
val = [6]
col = ["Transaction ID", "Payment Status", "Payment Date", "Patient Name"]
df = getDataFromDB(sql, val, col)
print(df)
