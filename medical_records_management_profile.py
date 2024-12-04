import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
from urllib.parse import parse_qs, urlparse
from dbconnect import getDataFromDB, modifyDB



  # Import your DB connection method
layout = html.Div(
    [
        dcc.Store(id='medicalresult_edit_id', storage_type='memory', data=0),
        dcc.Store(id='medicalpatientprofile_id', storage_type='memory', data=0),
        
        # Header and Back button
        dbc.Row(
            [
                dbc.Col(html.H2("Add New Medical Record", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/medical_records",
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "marginRight": "10px",
                            "backgroundColor": "#194D62"
                        }
                    ),
                    width="auto"
                ),
            ],
            align="center",
            className="mb-4"
        ),

        html.Hr(),

        # Form Layout
        dbc.Form(
            [
                # Appointment Dropdown
                dbc.Row(
                    [
                        dbc.Label("Select Recently Completed Appointment: ", style={"fontSize": "20px", "fontWeight": "bold"}),
                        dbc.Col(
                            dcc.Dropdown(
                                id='medicalresult_appointment',  # ID for the dropdown
                                placeholder='Select Appointment',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3",
                    id = 'appointment_dropdown_row'
                ),

                
                # Condition
                dbc.Row(
                    [
                        dbc.Label("Condition", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_condition',
                                placeholder='Enter Condition',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Diagnosis
                dbc.Row(
                    [
                        dbc.Label("Diagnosis", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_diagnosis',
                                placeholder='Enter Diagnosis',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Prescription
                dbc.Row(
                    [
                        dbc.Label("Prescription", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_prescription',
                                placeholder='Enter Prescription',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Treatment Done Dropdowns and Quantity Inputs
                dbc.Row(
                    [
                        dbc.Label("Treatment Done 1", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_done_1',
                                placeholder='Select Treatment 1',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_done_1_qty',
                                placeholder='Qty',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=2
                        ),
                    ],
                    className="mb-3"
                ),

                # Repeat for treatment_done_2 to treatment_done_5
                dbc.Row(
                    [
                        dbc.Label("Treatment Done 2", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_done_2',
                                placeholder='Select Treatment 2',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_done_2_qty',
                                placeholder='Qty',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=2
                        ),
                    ],
                    className="mb-3"
                ),
                 dbc.Row(
                    [
                        dbc.Label("Treatment Done 3", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_done_3',
                                placeholder='Select Treatment 3',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_done_3_qty',
                                placeholder='Qty',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=2
                        ),
                    ],
                    className="mb-3"
                ),
                 dbc.Row(
                    [
                        dbc.Label("Treatment Done 4", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_done_4',
                                placeholder='Select Treatment 4',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_done_4_qty',
                                placeholder='Qty',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=2
                        ),
                    ],
                    className="mb-3"
                ),
                 dbc.Row(
                    [
                        dbc.Label("Treatment Done 5", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_done_5',
                                placeholder='Select Treatment 1',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_done_5_qty',
                                placeholder='Qty',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=2
                        ),
                    ],
                    className="mb-3"
                ),
                 html.Div(
                    [
                       dbc.Checklist(
                            id='appointment_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[] 
                       )
                    ],
                    id='medicalresultprofile_deletediv'
                ),
                
                # Repeat for treatment_done_3, treatment_done_4, treatment_done_5 (similar to above)

                # Submit Button
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Submit", color="primary", className="mt-3", id='medicalresult_submit_button', style={
                                "borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white"}),
                            width="auto"
                        ),
                    ],
                    justify="start",
                    className="mt-3"
                ),

                # Alert for submission feedback
                dbc.Alert(id='medicalresult_submit_alert', is_open=False)
            ]
        ),
    ],
    className="container mt-4"
)
#removes dropdown during edit mode

# Callback to toggle appointment dropdown visibility based on mode
@app.callback(
    Output('appointment_dropdown_row', 'style'),
    
    Input('url', 'search')
)
def toggle_appointment_dropdown(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    if create_mode == 'edit':
        return {'display': 'none'} 
    elif create_mode == 'add':
        return {'display': 'block'} 
        


# Callback for loading treatment names from the database
@app.callback(
    [
        Output('treatment_done_1', 'options'),
        Output('treatment_done_2', 'options'),
        Output('treatment_done_3', 'options'),
        Output('treatment_done_4', 'options'),
        Output('treatment_done_5', 'options')
    ],
    Input('treatment_done_1', 'id')  # Triggered by any dropdown initialization
)
def load_treatment_names(_):
    # SQL query to fetch treatment names
    sql = """
        SELECT treatment_id, treatment_m AS treatment_name
        FROM treatment
    """
    # Fetch data from DB with empty values and columns lists
    df = getDataFromDB(sql, [], ["treatment_id", "treatment_name"])

    # Convert the fetched data into options for the dropdowns
    treatment_options = [{'label': row['treatment_name'], 'value': row['treatment_id']} for _, row in df.iterrows()]

    # Return the same options for each treatment dropdown
    return [treatment_options] * 5

#Gets patient ID or medical result from url
@app.callback(
    [Output('medicalpatientprofile_id', 'data')],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def medical_profile_load(pathname, urlsearch):

    if pathname == '/medical_records/medical_record_management_profile':
        # Parse the URL to extract the patient ID
        parsed = urlparse(urlsearch)
        medicalpatientprofile_id = parse_qs(parsed.query).get('id', [0])[0]
        return [medicalpatientprofile_id]  # Return patient ID to store it in memory
    else:
        raise PreventUpdate
#Puts Appointments without medical result pa sa options for the corresponding patient ID
@app.callback(
    [Output('medicalresult_appointment', 'options')],
    [Input('medicalpatientprofile_id', 'data')]  # Use the patient ID from the first callback
)
def load_all_appointments(medicalpatientprofile_id):
    
    if medicalpatientprofile_id:  # Check if the ID is not None or 0
        # SQL query to fetch appointments specific to the patient ID with proper date and time formatting
        sql = """
            SELECT appointment_id, 
                   TO_CHAR(appointment_date, 'DD, Month, YYYY') AS formatted_date,
                   TO_CHAR(appointment_time, 'HH12:MI AM') AS formatted_time
            FROM appointment
            WHERE patient_id = %s 
              AND (medical_result_id IS NULL OR medical_result_id = 0)  
        """
        # Fetch data from DB
        df = getDataFromDB(sql, [medicalpatientprofile_id], ["appointment_id", "formatted_date", "formatted_time"])

        # Convert the fetched data into options for the dropdown
        # Set 'label' to formatted date and time, and keep 'value' as appointment_id
        options = [
            {'label': f"{row['formatted_date']}, {row['formatted_time']}", 'value': row['appointment_id']}
            for _, row in df.iterrows()
        ]
        return [options]

    else:
        # If no patient ID, return an empty list or a default message
        return [[{'label': 'No appointments available', 'value': None}]]



#Removes Mark as delete during edit mode
@app.callback(
    [
        Output('medicalresult_edit_id', 'data'),
        Output('medicalresultprofile_deletediv', 'className'),
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def medical_result_load(pathname, urlsearch):
    if pathname == '/medical_records/medical_record_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            medical_edit_id = 0
            patient_profile_delete = 'd-none'
        else:
            medical_edit_id = int(parse_qs(parsed.query).get('id', [0])[0])
            patient_profile_delete = ''
        
        return [medical_edit_id, patient_profile_delete]
    
    else:
        raise PreventUpdate

#Adds to database
@app.callback(
    [Output('medicalresult_submit_alert', 'color'),
     Output('medicalresult_submit_alert', 'children'),
     Output('medicalresult_submit_alert', 'is_open')],
    [Input('medicalresult_submit_button', 'n_clicks')],
    [State('medicalresult_condition', 'value'),
     State('medicalresult_diagnosis', 'value'),
     State('medicalresult_prescription', 'value'),
     State('treatment_done_1', 'value'),
     State('treatment_done_1_qty', 'value'),
     State('treatment_done_2', 'value'),
     State('treatment_done_2_qty', 'value'),
     State('treatment_done_3', 'value'),
     State('treatment_done_3_qty', 'value'),
     State('treatment_done_4', 'value'),
     State('treatment_done_4_qty', 'value'),
     State('treatment_done_5', 'value'),
     State('treatment_done_5_qty', 'value'),
     State('medicalresult_appointment', 'value'),
     State('url', 'search'),
     State('medicalresult_edit_id', 'data')])
def submit_medical_result_form(n_clicks, condition, diagnosis, prescription, treatment_1, qty_1, treatment_2, qty_2, 
                                treatment_3, qty_3, treatment_4, qty_4, treatment_5, qty_5, appointment, urlsearch, edit_id):  
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    

    if not all([condition, diagnosis, prescription, treatment_1, qty_1,treatment_2,qty_2, treatment_3,qty_3, treatment_4,qty_4,treatment_5, qty_5]):
        return 'danger', 'Please fill in all required fields.', True

    try:
        if create_mode == 'add':
            
            
            # SQL to insert a new medical result
            sql = """INSERT INTO medical_result (medical_condition, medical_diagnosis, medical_prescription)
                     VALUES (%s, %s, %s)"""
            values = (condition, diagnosis, prescription)
            
            modifyDB(sql, values) 
            # SQL to find the max medical_result_id
            sql_find = """SELECT MAX(medical_result_id) FROM medical_result"""
            df_find = getDataFromDB(sql_find, [], ['Max Medical Result ID'])
            
            # Extract the value from the DataFrame
            result_id = int(df_find.iloc[0, 0])  # This will give you the value of id of medical result
            
            # SQL to update the Appointment with the new medical_result_id
            sql2 = """UPDATE Appointment
            SET medical_result_id = %s
            WHERE appointment_id = %s;"""
            values2 = (result_id, appointment)

            # Call the modifyDB function to execute the update
            modifyDB(sql2, values2)
        
            if treatment_1 and qty_1:
                sql_treatment_1 = """INSERT INTO Appointment_treatment (appointment_id, treatment_id, quantity)
                                      VALUES (%s, %s, %s);"""
                values_treatment_1 = (appointment, treatment_1, qty_1)
                modifyDB(sql_treatment_1, values_treatment_1)
            
            
            # Treatment 2
            if treatment_2 is not None and qty_2 is not None:
                sql_treatment_2 = """INSERT INTO Appointment_treatment (appointment_id, treatment_id, quantity)
                                    VALUES (%s, %s, %s);"""
                values_treatment_2 = (appointment, treatment_2, qty_2)
                modifyDB(sql_treatment_2, values_treatment_2)
            

            # Treatment 3
            if treatment_3 is not None and qty_3 is not None:
                sql_treatment_3 = """INSERT INTO Appointment_treatment (appointment_id, treatment_id, quantity)
                                    VALUES (%s, %s, %s);"""
                values_treatment_3 = (appointment, treatment_3, qty_3)
                modifyDB(sql_treatment_3, values_treatment_3)
            
            # Treatment 4
            if treatment_4 is not None and qty_4 is not None:
                sql_treatment_4 = """INSERT INTO Appointment_treatment (appointment_id, treatment_id, quantity)
                                    VALUES (%s, %s, %s);"""
                values_treatment_4 = (appointment, treatment_4, qty_4)
                modifyDB(sql_treatment_4, values_treatment_4)
            

            # Treatment 5
            if treatment_5 is not None and qty_5 is not None:
                sql_treatment_5 = """INSERT INTO Appointment_treatment (appointment_id, treatment_id, quantity)
                                    VALUES (%s, %s, %s);"""
                values_treatment_5 = (appointment, treatment_5, qty_5)
                modifyDB(sql_treatment_5, values_treatment_5)
            
                
        elif create_mode == 'edit':
            # SQL to update the medical result (Conditon to prescription)
        
            sql1 = """UPDATE medical_result
                     SET medical_condition = %s,
                         medical_diagnosis = %s,
                         medical_prescription = %s
                     WHERE medical_result_id = %s;"""
            values1 = [condition, diagnosis, prescription, edit_id]

            modifyDB(sql1, values1)
            
            #Get The appointment ID
            sql_find1 = """SELECT appointment_id 
                           FROM Appointment 
                           WHERE medical_result_id = %s;"""
            
            df_find1 = getDataFromDB(sql_find1, [edit_id], ['appointment_id'])
            
            # Extract the value from the DataFrame
            appointment_id= int(df_find1.iloc[0, 0])  # This will give you the value of id of medical result

            #Getting the IDs of the appointment_treatment

            sql_find2 = """SELECT appointment_treatment_id
               FROM appointment_treatment
               WHERE appointment_id = %s;"""

            # Fetch data into a DataFrame
            df_find2 = getDataFromDB(sql_find2, [appointment_id], ['appointment_treatment_id'])

            # Access up to 5 appointment_treatment_id values from the DataFrame using .iloc
            appointment_treatment_id_1 = int(df_find2.iloc[0, 0])
            appointment_treatment_id_2 = int(df_find2.iloc[1, 0])
            appointment_treatment_id_3 = int(df_find2.iloc[2, 0]) 
            appointment_treatment_id_4 = int(df_find2.iloc[3, 0]) 
            appointment_treatment_id_5 = int(df_find2.iloc[4, 0])

            #Treatment 1
            if treatment_1 and qty_1:
                sql_treatment_1 = """UPDATE Appointment_treatment
                                      SET 
                                        treatment_id = %s,
                                        quantity = %s
                                        WHERE appointment_treatment_id = %s;"""
                values_treatment_1 = (treatment_1, qty_1,appointment_treatment_id_1)
                modifyDB(sql_treatment_1, values_treatment_1)
            
           
            # Treatment 2
            if treatment_2 and qty_2:
                sql_treatment_2 = """UPDATE Appointment_treatment
                                        SET 
                                            treatment_id = %s,
                                            quantity = %s
                                        WHERE appointment_treatment_id = %s;"""
                values_treatment_2 = (treatment_2, qty_2, appointment_treatment_id_2)
                modifyDB(sql_treatment_2, values_treatment_2)

            

            # Treatment 3
            if treatment_3 and qty_3:
                sql_treatment_3 = """UPDATE Appointment_treatment
                                        SET 
                                            treatment_id = %s,
                                            quantity = %s
                                        WHERE appointment_treatment_id = %s;"""
                values_treatment_3 = (treatment_3, qty_3, appointment_treatment_id_3)
                modifyDB(sql_treatment_3, values_treatment_3)

            

            # Treatment 4
            if treatment_4 and qty_4:
                sql_treatment_4 = """UPDATE Appointment_treatment
                                        SET 
                                            treatment_id = %s,
                                            quantity = %s
                                        WHERE appointment_treatment_id = %s;"""
                values_treatment_4 = (treatment_4, qty_4, appointment_treatment_id_4)
                modifyDB(sql_treatment_4, values_treatment_4)

            

            # Treatment 5
            if treatment_5 and qty_5:
                sql_treatment_5 = """UPDATE Appointment_treatment
                                        SET 
                                            treatment_id = %s,
                                            quantity = %s
                                        WHERE appointment_treatment_id = %s;"""
                values_treatment_5 = (treatment_5, qty_5, appointment_treatment_id_5)
                modifyDB(sql_treatment_5, values_treatment_5)
            
        return 'success', 'Medical Result Submitted successfully!', True
        
   
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True

# Prepopulate data when editing

@app.callback(
    [
        Output('medicalresult_condition', 'value'),
        Output('medicalresult_diagnosis', 'value'),
        Output('medicalresult_prescription', 'value'),
        Output('treatment_done_1', 'value'),
        Output('treatment_done_1_qty', 'value'),
        Output('treatment_done_2', 'value'),
        Output('treatment_done_2_qty', 'value'),
        Output('treatment_done_3', 'value'),
        Output('treatment_done_3_qty', 'value'),
        Output('treatment_done_4', 'value'),
        Output('treatment_done_4_qty', 'value'),
        Output('treatment_done_5', 'value'),
        Output('treatment_done_5_qty', 'value'),
    ],
    [Input('medicalpatientprofile_id', 'modified_timestamp')],
    [State('medicalresult_edit_id', 'data')]
)

def populate_medical_record(timestamp,medicalresult_edit_id):
    if medicalresult_edit_id > 0:
       


        sql_find1 = """SELECT medical_condition, medical_diagnosis, medical_prescription
                        FROM Medical_result
                        WHERE medical_result_id = %s;"""
        
        values_find1 = [medicalresult_edit_id]
        col_find1 = ['medical_condition', 'medical_diagnosis', 'medical_prescription']

        df_find1 = getDataFromDB(sql_find1, values_find1, col_find1)

        condition = df_find1['medical_condition'][0]
        diagnosis = df_find1['medical_diagnosis'][0]
        prescription = df_find1['medical_prescription'][0]          
        
        #Get The appointment ID
        sql_find2 = """SELECT appointment_id 
                        FROM Appointment 
                        WHERE medical_result_id = %s;"""
        
        df_find2 = getDataFromDB(sql_find2, [medicalresult_edit_id], ['appointment_id'])
        
        # Extract the value from the DataFrame
        appointment_id= int(df_find2.iloc[0, 0])  # This will give you the value of id of medical result

        #Getting the IDs of the appointment_treatment

        sql_find3 = """SELECT appointment_treatment_id
            FROM appointment_treatment
            WHERE appointment_id = %s;"""

        # Fetch data into a DataFrame
        df_find3 = getDataFromDB(sql_find3, [appointment_id], ['appointment_treatment_id'])

        # Access up to 5 appointment_treatment_id values from the DataFrame using .iloc
        appointment_treatment_id_1 = int(df_find3.iloc[0, 0])
        appointment_treatment_id_2 = int(df_find3.iloc[1, 0])
        appointment_treatment_id_3 = int(df_find3.iloc[2, 0]) 
        appointment_treatment_id_4 = int(df_find3.iloc[3, 0]) 
        appointment_treatment_id_5 = int(df_find3.iloc[4, 0])

        sql_findt1 = """SELECT treatment_id, quantity
                        FROM appointment_treatment
                        WHERE appointment_treatment_id =%s"""
        
        values_findt1 = [appointment_treatment_id_1]

        col_findt1 = ['treatment_id', 'quantity']

        df_findt1 = getDataFromDB(sql_findt1, values_findt1, col_findt1)

        treatment_name_id1 = df_findt1['treatment_id'][0]
        quantity_1 = df_findt1['quantity'][0]

        sql_findt2 = """SELECT treatment_id, quantity
                        FROM appointment_treatment
                        WHERE appointment_treatment_id =%s"""
        
        values_findt2 = [appointment_treatment_id_2]

        col_findt2 = ['treatment_id', 'quantity']

        df_findt2 = getDataFromDB(sql_findt2, values_findt2, col_findt2)

        treatment_name_id2 = df_findt2['treatment_id'][0]
        quantity_2 = df_findt2['quantity'][0]

        sql_findt3 = """SELECT treatment_id, quantity
                FROM appointment_treatment
                WHERE appointment_treatment_id = %s"""
        values_findt3 = [appointment_treatment_id_3]
        col_findt3 = ['treatment_id', 'quantity']
        df_findt3 = getDataFromDB(sql_findt3, values_findt3, col_findt3)

        treatment_name_id3 = df_findt3['treatment_id'][0]
        quantity_3 = df_findt3['quantity'][0]

        sql_findt4 = """SELECT treatment_id, quantity
                        FROM appointment_treatment
                        WHERE appointment_treatment_id = %s"""
        values_findt4 = [appointment_treatment_id_4]
        col_findt4 = ['treatment_id', 'quantity']
        df_findt4 = getDataFromDB(sql_findt4, values_findt4, col_findt4)
        treatment_name_id4 = df_findt4['treatment_id'][0]
        quantity_4 = df_findt4['quantity'][0]

        sql_findt5 = """SELECT treatment_id, quantity
                        FROM appointment_treatment
                        WHERE appointment_treatment_id = %s"""
        values_findt5 = [appointment_treatment_id_5]
        col_findt5 = ['treatment_id', 'quantity']
        df_findt5 = getDataFromDB(sql_findt5, values_findt5, col_findt5)
        treatment_name_id5 = df_findt5['treatment_id'][0]
        quantity_5 = df_findt5['quantity'][0]
         
        

        return condition, diagnosis, prescription,treatment_name_id1, quantity_1,treatment_name_id2, quantity_2,treatment_name_id3, quantity_3,treatment_name_id4, quantity_4,treatment_name_id5, quantity_5
    else:
        raise PreventUpdate
