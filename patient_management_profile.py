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
        dcc.Store(id='patientprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2("Add New Patient Profile", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/patient_profile",
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
                
                # Birthdate
                dbc.Row(
                    [
                        dbc.Label("Birthdate", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='birthdate',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Age
                dbc.Row(
                    [
                        dbc.Label("Age", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='age',
                                placeholder='Enter Age',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Sex
                dbc.Row(
                    [
                        dbc.Label("Sex", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='sex',
                                options=[
                                    {'label': 'Male', 'value': 'Male'},
                                    {'label': 'Female', 'value': 'Female'},
                                    {'label': 'Other', 'value': 'Other'}
                                ],
                                placeholder='Select Sex',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Cellphone Number
                dbc.Row(
                    [
                        dbc.Label("Cellphone Number", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='tel',
                                id='cellphone_number',
                                placeholder='Enter Cellphone Number',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Email Address
                dbc.Row(
                    [
                        dbc.Label("Email Address", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='email',
                                id='email_address',
                                placeholder='Enter Email Address',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Street
                dbc.Row(
                    [
                        dbc.Label("Street", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='street',
                                placeholder='Enter Street',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Barangay
                dbc.Row(
                    [
                        dbc.Label("Barangay", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='barangay',
                                placeholder='Enter Barangay',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # City
                dbc.Row(
                    [
                        dbc.Label("City", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='city',
                                placeholder='Enter City',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Postal Code
                dbc.Row(
                    [
                        dbc.Label("Postal Code", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='postal_code',
                                placeholder='Enter Postal Code',
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
                            id='patient_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='patientprofile_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3",
                    id='submit_button',
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
        Output('patientprofile_id', 'data'),
        Output('patientprofile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def patient_profile_load(pathname, urlsearch):
    if pathname == '/patient_profile/patient_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            patientprofile_id = 0
            deletediv = 'd-none'
            
        else:
            patientprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            deletediv =''
        
        return [patientprofile_id, deletediv]
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
     State('birthdate', 'value'),
     State('age', 'value'),
     State('sex', 'value'),
     State('cellphone_number', 'value'),
     State('email_address', 'value'),
     State('street', 'value'),
     State('barangay', 'value'),
     State('city', 'value'),
     State('postal_code', 'value'),
     State('url', 'search'),
     State('patientprofile_id', 'data')]
)
def submit_form(n_clicks, last_name, first_name, middle_name, birthdate, age, sex, cellphone_number, 
                email_address, street, barangay, city, postal_code, urlsearch, patientprofile_id):
    
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([last_name, first_name, birthdate, age, sex, cellphone_number, email_address, street, barangay, city, postal_code]):
        return 'danger', 'Please fill in all required fields.', True

    # SQL to insert or update the database
    if create_mode == 'add':
        sql = """INSERT INTO patient (patient_last_m, patient_first_m, patient_middle_m, patient_bd, age,
                sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE);"""
        
        values = [last_name, first_name, middle_name, birthdate, age, sex, cellphone_number, 
                  email_address, street, barangay, city, postal_code]
    
    elif create_mode == 'edit':
        sql = """UPDATE patient
                SET patient_last_m = %s,
                    patient_first_m = %s,
                    patient_middle_m = %s,
                    patient_bd = %s,
                    age = %s,
                    sex = %s,
                    patient_cn = %s,
                    patient_email = %s,
                    street = %s,
                    barangay = %s,
                    city = %s,
                    postal_code = %s
                WHERE patient_id = %s;"""
        
        values = [last_name, first_name, middle_name, birthdate, age, sex, cellphone_number, 
                  email_address, street, barangay, city, postal_code, patientprofile_id]
    else:
        raise PreventUpdate

    try:
        modifyDB(sql, values)
        return 'success', 'Patient Profile Submitted successfully!', True
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True

@app.callback(
    [Output('last_name', 'value'),
    Output('first_name', 'value'),
    Output('middle_name', 'value'),
    Output('birthdate', 'value'),
    Output('age', 'value'),
    Output('sex', 'value'),
    Output('cellphone_number', 'value'),
    Output('email_address', 'value'),
    Output('street', 'value'),
    Output('barangay', 'value'),
    Output('city', 'value'),
    Output('postal_code', 'value'),
    ],
    [Input('patientprofile_id', 'modified_timestamp'),],

    [State('patientprofile_id', 'data'),]
)
def patient_profile_populate(timestamp, patientprofile_id):
    if patientprofile_id > 0:
        sql = """SELECT patient_last_m, patient_first_m, patient_middle_m, patient_bd, age,
                sex, patient_cn, patient_email, street, barangay, city, postal_code
                FROM patient
                WHERE patient_id = %s"""
        values = [patientprofile_id]
        col = ['last_name', 'first_name', 'middle_name', 'birthdate', 'age', 'sex', 'cellphone_number', 
               'email_address', 'street', 'barangay', 'city', 'postal_code']

        df = getDataFromDB(sql, values, col)

        lastname = df['last_name'][0]
        firstname = df['first_name'][0]
        middlename = df['middle_name'][0]
        birthdate = df['birthdate'][0]
        age = df['age'][0]
        sex = df['sex'][0]
        cellphonenumber = df['cellphone_number'][0]
        emailaddress = df['email_address'][0]
        street = df['street'][0]
        barangay = df['barangay'][0]
        city = df['city'][0]
        postal_code = df['postal_code'][0]

        return [
            lastname, firstname, middlename, birthdate, age, sex,
            cellphonenumber, emailaddress, street, barangay, city, postal_code]
    else:
        raise PreventUpdate
