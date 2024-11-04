import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    [
        html.H2('Patient Profiles'),  # Page Header
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H3('Manage Patient Profiles')),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Add New Patient Profile",
                                    href='/patient_manager/patient_manager_profile?mode=add',
                                    outline=True, color="primary", 
                                    className="me-1"
                                ),
                                dbc.Button(
                                    "Update Existing Patient Profile",
                                    href='/patientrecords/updateexistingrecord',outline=True,
                                    color="primary",
                                    className="me-1"
                                ),
                                dbc.Button(
                                    "Delete Patient Profile",
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
                                html.H4('Search Patient Profile'),
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
                                    "The Patient profile will be displayed in a table after pressing the search button.",
                                    id='patient_list1',
                                    className="mt-3"
                                ),
                                 html.Div(
                                    "The table will include patient_ID, patient name, contact details, latest appointment, and payment status",
                                    id='patient_list2',
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

