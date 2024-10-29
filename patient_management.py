import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    [
        html.H2('Patient Records'),  # Page Header
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H3('Manage Patient Records')),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Add New Record",
                                    href='/patientrecords/addnewrecord',
                                    outline=True, color="primary", 
                                    className="me-1"
                                ),
                                dbc.Button(
                                    "Update Existing Record",
                                    href='/patientrecords/updateexistingrecord',outline=True,
                                    color="primary",
                                    className="me-1"
                                ),
                                dbc.Button(
                                    "Delete Record",
                                    href='/patientrecords/deleterecord',outline=True,
                                    color="danger",
                                    className="me-1"
                                )
                            ],
                            className="d-flex justify-content-start"
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Search Patient'),
                                dbc.Form(
                                    dbc.Row(
                                        [
                                            dbc.Label("Patient Name", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id='patient_name',
                                                    placeholder='Enter Patient Name'
                                                ),
                                                width=6
                                            ),
                                            dbc.Col(
                                                dbc.Button("Search", color="primary"),
                                                width="auto"
                                            )
                                        ],
                                        className="g-2"
                                    )
                                ),
                                html.Div(
                                    "Table of patient records will go here.",
                                    id='patient_list',
                                    className="mt-3"
                                )
                            ]
                        )
                    ]
                )
            ],
            className="shadow-sm"
        )
    ],
    className="container mt-4"
)