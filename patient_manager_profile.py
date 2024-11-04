import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from dbconnect import getDataFromDB, modifyDB



# New layout for adding a patient record
layout = html.Div(
    [
        html.H2("Add New Patient Profile"),
        html.Hr(),
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
                                placeholder='Enter Last Name'
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
                                placeholder='Enter First Name'
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
                                placeholder='Enter Middle Name'
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
                                id='birthdate'
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
                                placeholder='Enter Age'
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
                                placeholder='Select Sex'
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
                                placeholder='Enter Cellphone Number'
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
                                placeholder='Enter Email Address'
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
                                placeholder='Enter Street'
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
                                placeholder='Enter Barangay'
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
                                placeholder='Enter City'
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
                                placeholder='Enter Postal Code'
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Submit Button
                dbc.Button("Submit", color="primary", className="mt-3")
            ]
        )
    ],
    className="container mt-4"
)

