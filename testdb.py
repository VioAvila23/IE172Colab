import dbconnect as db
from dbconnect import getDataFromDB, modifyDB

# Get the appointment Date and Time
sql_appointment = """SELECT TO_CHAR(appointment_date, 'DD, Month, YYYY') AS appointment_date, 
                        TO_CHAR(appointment_time, 'HH12:MI AM') AS appointment_time
                     FROM Appointment
                     WHERE medical_result_id = %s"""
value_appointment = [7]
col = ['appointment_date', 'appointment_time']

df = getDataFromDB(sql_appointment, value_appointment, col)

# Extract Date and Time
appointment_date = df['appointment_date'][0]
apointment_time = df['appointment_time'][0]

# Print Date and Time
x = (f"{appointment_date} {apointment_time}")

if __name__ == '__main__':
    print(x)
