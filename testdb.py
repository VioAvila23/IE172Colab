import dbconnect as db




def getGenresTable():
    sqlcode = """ Select patient.patient_id as "Patient ID", concat(patient.patient_first_m,' ', patient.patient_middle_m,' ', patient.patient_last_m) as "Patient Name",
        age, patient.patient_id

        FROM patient

        ORDER BY patient.patient_id"""    

    values = [] # we do not have any %s in the SQL
    cols = ['id', 'name', 'modified_on','patientid'] # these are column names for the table
   
    # the table is stored in variable genres_db as a dataframe 
    genres_db = db.getDataFromDB(sqlcode, values, cols)
    
    return genres_db

    


if __name__ == '__main__':

    print(getGenresTable())