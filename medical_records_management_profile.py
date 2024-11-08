import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs, urlparse

layout = html.Div(
    [
        dcc.Store(id='medical_edit_id', storage_type='memory', data=0),
        
        # Header and Back button
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        id="header_text",
                        style={'font-size': '25px'}
                    ),
                    width="auto"
                ),
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
                # Appointment Date
                dbc.Row(
                    [
                        dbc.Label("Date", width=2),
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
              
             
                # Treatment Done
                dbc.Row(
                    [
                        dbc.Label("Treatment Done", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='treatment_done',
                                placeholder='Enter Treatment Done',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Condition
                dbc.Row(
                    [
                        dbc.Label("Condition", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='condition',
                                options=[
                                    {'label': 'Remarkable', 'value': 'Remarkable'},
                                    {'label': 'Unremarkable', 'value': 'Unremarkable'}
                                ],
                                placeholder='Select Condition',
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
                                id='diagnosis',
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
                                id='prescription',
                                placeholder='Enter Prescription',
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
                    id='medicalresult_deletediv'
                ),

                # Submit Button
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
        
        # Alert for submission feedback
        dbc.Alert(id='submit_alert', is_open=False)
    ],
    className="container mt-4"
)


@app.callback(
    [
        Output('medical_edit_id', 'data'),
        Output('patient_profile_delete', 'className'),
        Output('header_text', 'children')
    ],
    [Input('url', 'pathname'),],
    [State('url', 'search'),]
)

def medical_result_load(pathname,urlsearch):
    if pathname == '/medical_records/medical_record_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            medical_edit_id = 0
            patient_profile_delete = 'd-none'
            header_text = "Add New Medical Record"
            

        else:
            medical_edit_id = int(parse_qs(parsed.query).get('id', [0])[0])
            patient_profile_delete = ''
            header_text = "Edit Medical Record"
        
        return [medical_edit_id, patient_profile_delete, header_text]
    
    else:
        raise PreventUpdate
