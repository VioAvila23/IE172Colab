import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from app import app
from dbconnect import getDataFromDB

layout = html.Div(
    [
        # Header with Back Button
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
        )
    ],
    className="container mt-4"
)
