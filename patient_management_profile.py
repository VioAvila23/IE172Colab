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
                
                # Mark as Deleted (only visible in edit mode)
                html.Div(
                    [
                        dbc.Checklist(
                            id='patient_profile_delete',
                            options=[{'value': 1, 'label': "Mark as Deleted"}],
                            value=[]
                        )
                    ],
                    id='delete_checkbox_div'
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
        Output('delete_checkbox_div', 'style')
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
            delete_checkbox_style = {'display': 'none'}  # Hide checkbox in add mode
        else:
            patientprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            delete_checkbox_style = {'display': 'block'}  # Show checkbox in edit mode
        
        return [patientprofile_id, delete_checkbox_style]
    else:
        raise PreventUpdate
