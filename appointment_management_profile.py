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
                dbc.Col(html.H2("Schedule New Appointment", style={'font-size': '25px'}), width="auto"),
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
                # Last Name
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='last_name',
                                placeholder='Enter Last Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # First Name
                dbc.Row(
                    [
                        dbc.Label("First Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='first_name',
                                placeholder='Enter First Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Middle Name
                dbc.Row(
                    [
                        dbc.Label("Middle Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='middle_name',
                                placeholder='Enter Middle Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
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
                                    {'label': 'Booked', 'value': 'Booked'},
                                    {'label': 'Pending', 'value': 'Pending'},
                                    {'label': 'Complete', 'value': 'Complete'},
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
        dbc.Alert(id='submit_alert', is_open=False)
    ],
    className="container mt-4"
)

@app.callback(
    [
        Output('appointmentprofile_id', 'data'),
        Output('appointmentprofile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def patient_profile_load(pathname, urlsearch):
    if pathname == '/appointment/appointment_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            appointmentprofile_id = 0
            deletediv = 'd-none'
            
        else:
            appointmentprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv =''
        
        return [appointmentprofile_id, deletediv]
    else:
        raise PreventUpdate

@app.callback(
    [Output('submit_alert', 'color'),
     Output('submit_alert', 'children'),
     Output('submit_alert', 'is_open')],
    [Input('submit_button', 'n_clicks')],
    [State('last_name', 'value'),
     State('first_name', 'value'),
     State('middle_name', 'value'),
     State('appointment_date', 'value'),
     State('appointment_time', 'value'),
     State('appointment_reason', 'value'),
     State('appointment_status', 'value'),
     State('url', 'search'),
     State('patientprofile_id', 'data')]
)
def submit_form(n_clicks, last_name, first_name, middle_name, appointment_date, appointment_time, appointment_reason, appointment_status, 
                urlsearch, appointmentprofile_id):
    
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([last_name, first_name, last_name, first_name, middle_name, appointment_date, appointment_time, appointment_reason, appointment_status]):
        return 'danger', 'Please fill in all required fields.', True

    # SQL to insert or update the database
    if create_mode == 'add':
        sql = """INSERT INTO patient (patient_last_m, patient_first_m, patient_middle_m, appointment_date, appointment_time,
                appointment_reason, appointment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        values = [last_name, first_name, middle_name, appointment_date, appointment_time, appointment_reason, appointment_status]
    
    elif create_mode == 'edit':
        sql = """UPDATE patient
                SET patient_last_m = %s,
                    patient_first_m = %s,
                    patient_middle_m = %s,
                    appointment_date = %s,
                    appointment_time = %s,
                    appointment_reason = %s,
                    appointment_status = %s,
                WHERE appointment_id = %s;"""
        
        values = [last_name, first_name, middle_name, appointment_date, appointment_time, appointment_reason, appointment_status]

    else:
        raise PreventUpdate

    try:
        modifyDB(sql, values)
        return 'success', 'Appointment Schedule Submitted successfully!', True
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True

@app.callback(
    [Output('last_name', 'value'),
    Output('first_name', 'value'),
    Output('middle_name', 'value'),
    Output('appointment_date', 'value'),
    Output('appointment_time', 'value'),
    Output('appointment_reason', 'value'),
    Output('appointment_status', 'value'),
    ],
    [Input('appointmentprofile_id', 'modified_timestamp'),],

    [State('appointmentprofile_id', 'data'),]
)
def appointment_profile_populate(timestamp, appointmentprofile_id):
    if appointmentprofile_id > 0:
        sql = """SELECT patient_last_m, patient_first_m, patient_middle_m, appointment_date, appointment_time,
                appointment_reason, appointment_status
                FROM appointment
                WHERE appointment_id = %s"""
        values = [appointmentprofile_id]
        col = ['last_name', 'first_name', 'middle_name', 'appointment_date', 'appointment_time', 'appointment_reason', 'appointment_status']

        df = getDataFromDB(sql, values, col)

        lastname = df['last_name'][0]
        firstname = df['first_name'][0]
        middlename = df['middle_name'][0]
        appointmentdate = df['appointment_date'][0]
        appointmenttime = df['appointment_time'][0]
        appointmentreason = df['appointment_reason'][0]
        appointmentstatus = df['appointment_status'][0]

        return [last_name, first_name, middle_name, appointment_date, appointment_time, appointment_reason, appointment_status]
    else:
        raise PreventUpdate
