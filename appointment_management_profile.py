from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dash import Input, Output, State
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate

layout = html.Div(
    [
        dcc.Store(id='appointmentprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        id="appointment_header",
                        style={'font-size': '25px'}
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/appointment",
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
                # Patient Name Dropdown (Dynamic)
                dbc.Row(
                    [
                        dbc.Label("Patient Name", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='patient_name_dropdown_appointment',
                                placeholder='Select Patient Name',
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),
                
                # Appointment Date
                dbc.Row(
                    [
                        dbc.Label("Appointment Date", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='appointment_date',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Appointment Time
                dbc.Row(
                    [
                        dbc.Label("Appointment Time", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='time',
                                id='appointment_time',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Appointment Reason
                dbc.Row(
                    [
                        dbc.Label("Appointment Reason", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='appointment_reason',
                                placeholder='Enter Appointment Reason',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),             
                
                # Appointment Status
                dbc.Row(
                    [
                        dbc.Label("Appointment Status", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='appointment_status',
                                options=[
                                    {'label': 'Scheduled', 'value': 'Scheduled'},
                                    {'label': 'Pending', 'value': 'Pending'},
                                    {'label': 'Completed', 'value': 'Completed'},
                                ],
                                placeholder='Select Status',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
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
                    id='appointmentprofile_deletediv'
                ),

                # Submit Button
                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3",
                    id = 'appointmentsubmit_button',
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                )
            ]
        ),
        dbc.Alert(id='appointmentsubmit_alert', is_open=False)
    ],
    className="container mt-4"
)

# Callback to update the header dynamically
@app.callback(
    Output('appointment_header', 'children'),
    Input('appointmentprofile_id', 'data')
)
def update_header(appointment_id):
    if appointment_id == 0:
        return "Schedule New Appointment"
    else:
        return "Reschedule Appointment"

@app.callback(
    Output('patient_name_dropdown_appointment', 'options'),
    [Input('appointmentprofile_id', 'data')],
)
def load_patient_names_appointment(appointmentprofile_id):
    # SQL query to fetch active patient names
    sql_active_patients = """
        SELECT patient_id, CONCAT(patient_last_m, ', ', patient_first_m) AS patient_name
        FROM patient
        WHERE patient_delete = FALSE
    """

    # Fetch active patients
    df_active = getDataFromDB(sql_active_patients, [], ["patient_id", "patient_name"])
    
    options = [{'label': row['patient_name'], 'value': row['patient_id']} for _, row in df_active.iterrows()]

    # If in edit mode and there is a specific appointment ID, fetch the associated deleted patient (if applicable)
    if appointmentprofile_id > 0:
        sql_deleted_patient = """
            SELECT patient_id, CONCAT(patient_last_m, ', ', patient_first_m) AS patient_name
            FROM patient
            WHERE patient_id = (
                SELECT patient_id 
                FROM Appointment 
                WHERE appointment_id = %s
            )
        """
        df_deleted = getDataFromDB(sql_deleted_patient, [appointmentprofile_id], ["patient_id", "patient_name"])
        
        # Add the deleted patient to the dropdown options (if it exists and is not already present)
        if not df_deleted.empty:
            deleted_patient_option = {
                'label': df_deleted['patient_name'][0], 
                'value': df_deleted['patient_id'][0]
            }
            if deleted_patient_option not in options:
                options.append(deleted_patient_option)

    return options

#Hides Mark as Delete During Add Mode
@app.callback(
    [
        Output('appointmentprofile_id', 'data'),
        Output('appointmentprofile_deletediv', 'className'),
    ],
    [Input('url', 'pathname'),],
    [State('url', 'search'),]
)

def appointment_result_load(pathname,urlsearch):
    if pathname == '/appointments/appointment_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            appointmentprofile_id = 0
            appointmentprofile_deletediv ='d-none'
        
        else:
            appointmentprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            appointmentprofile_deletediv = ''
        
        return [appointmentprofile_id, appointmentprofile_deletediv]

    else:
         raise PreventUpdate
@app.callback(
    [Output('appointmentsubmit_alert', 'color'),
     Output('appointmentsubmit_alert', 'children'),
     Output('appointmentsubmit_alert', 'is_open')],
    [Input('appointmentsubmit_button', 'n_clicks')],
    [State('patient_name_dropdown_appointment', 'value'),
     State('appointment_date', 'value'),
     State('appointment_time', 'value'),
     State('appointment_reason', 'value'),
     State('appointment_status', 'value'),
     State('url', 'search'),
     State('appointmentprofile_id', 'data'),
     State('appointment_profile_delete', 'value')]
)
def submit_appointment_form(n_clicks, patient_name, appointment_date, appointment_time, appointment_reason, 
                            appointment_status, urlsearch, appointmentprofile_id, delete):

    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    # Determine the mode: Add or Edit
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Validate required fields for add/edit mode (not for delete)
    if not delete and not all([patient_name, appointment_date, appointment_time, appointment_reason, appointment_status]):
        return 'danger', 'Please fill in all required fields.', True

    # Check for existing appointment conflicts (ignoring patient_id)
    if not delete:  # Skip conflict check if delete is selected
        conflict_sql = """
            SELECT COUNT(*) 
            FROM Appointment
            WHERE appointment_date = %s 
              AND appointment_time = %s
              AND NOT appointment_delete
              AND appointment_status != 'Completed'
        """
        conflict_values = [appointment_date, appointment_time]

        if create_mode == 'edit':
            conflict_sql += " AND appointment_id <> %s"  # Exclude the current appointment in edit mode
            conflict_values.append(appointmentprofile_id)

        # Query the database to check for conflicts
        conflict_result = getDataFromDB(conflict_sql, conflict_values, ['count'])

        if conflict_result['count'][0] > 0:
            return 'danger', 'The selected schedule is already taken. Please choose another date or time.', True

    # SQL to insert or update the database
    if create_mode == 'add':
        # Insert a new record into the Appointment table
        sql = """INSERT INTO Appointment (patient_id, appointment_date, appointment_time, appointment_reason, appointment_status)
                 VALUES (%s, %s, %s, %s, %s)"""
        values = [patient_name, appointment_date, appointment_time, appointment_reason, appointment_status]

    elif create_mode == 'edit':
        if delete:
            # Mark the appointment as deleted
            sql = """UPDATE Appointment
                     SET appointment_delete = TRUE
                     WHERE appointment_id = %s"""
            values = [appointmentprofile_id]
        else:
            # Update the existing record
            sql = """UPDATE Appointment
                     SET patient_id = %s,
                         appointment_date = %s,
                         appointment_time = %s,
                         appointment_reason = %s,
                         appointment_status = %s
                     WHERE appointment_id = %s"""
            values = [patient_name, appointment_date, appointment_time, appointment_reason, appointment_status, appointmentprofile_id]
    else:
        raise PreventUpdate

    # Execute database modification
    try:
        modifyDB(sql, values)
        if delete:
            return 'warning', 'Appointment Deleted', True
        return 'success', 'Appointment Submitted Successfully!', True
    except Exception as e:
        return 'danger', f'Error occurred: {e}', True



# Prepopulate data for the appointment form, including patient name
# Prepopulate data for the appointment form, including patient name and appointment status
@app.callback(
    [Output('patient_name_dropdown_appointment', 'value'),
     Output('appointment_date', 'value'),
     Output('appointment_time', 'value'),
     Output('appointment_reason', 'value'),
     Output('appointment_status', 'value')],  # Added appointment_status to outputs
    [Input('appointmentprofile_id', 'modified_timestamp')],
    [State('appointmentprofile_id', 'data')]
)
def appointment_profile_populate(timestamp, appointmentprofile_id):
    if appointmentprofile_id > 0:
        # Query to fetch appointment details, patient name, and status
        sql = """SELECT p.patient_id, p.patient_first_m, p.patient_last_m, 
                         a.appointment_date, a.appointment_time, a.appointment_reason, a.appointment_status
                 FROM Appointment a
                 JOIN Patient p ON a.patient_id = p.patient_id
                 WHERE a.appointment_id = %s"""
        values = [appointmentprofile_id]
        col = ['patient_id', 'patient_first_m', 'patient_last_m', 
               'appointment_date', 'appointment_time', 'appointment_reason', 'appointment_status']

        # Fetch the data from the database
        df = getDataFromDB(sql, values, col)

        # Prepare the patient name and ID
        patient_name = f"{df['patient_first_m'][0]} {df['patient_last_m'][0]}"
        patient_id = df['patient_id'][0]

        # Extract other appointment details
        appointment_date = df['appointment_date'][0]
        appointment_time = df['appointment_time'][0]
        appointment_reason = df['appointment_reason'][0]
        appointment_status = df['appointment_status'][0]

        # Return the preselected patient ID and other appointment details
        return patient_id, appointment_date, appointment_time, appointment_reason, appointment_status
    else:
        raise PreventUpdate

