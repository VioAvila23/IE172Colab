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


