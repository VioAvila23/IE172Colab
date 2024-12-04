from urllib.parse import urlparse, parse_qs
URL='http://127.0.0.1:8050/medical_records/medical_record_management_profile?mode=add&id=1'


    # Step 1: Extract patient_id from the URL
parsed_url = urlparse(URL)
    
    # Step 2: Get the query parameters as a dictionary
dict = parse_qs(parsed_url.query)
    
    # Step 3: Extract the 'id' from the query parameters (since your URL has id=1)
patient_id = dict.get('id', [None])[0]

print(patient_id)