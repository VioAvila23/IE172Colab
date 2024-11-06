import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, dcc, html
from app import app
from dbconnect import getDataFromDB

layout = dbc.Container(
    [
        # Row for search bar and Add New Patient button
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Search Patient Name", 
                            className="form-label", 
                            style={"fontSize": "20px", "fontWeight": "bold"}  # Larger font size for label
                        ),
                        dcc.Input(
                            id="search_patient_name",  # ID for search bar
                            type="text",
                            placeholder="Enter patient name...",
                            className="form-control",
                            style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}  # Larger font size for input text
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    dbc.Button(
                        "Add New Patient",
                        href = '/patient_profile/patient_management_profile?mode=add',
                        style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white"},  # Custom button color and text color
                        className="float-end"
                    ),
                    md=4,
                    style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
                ),
            ],
            className="mb-4",
            align="center"
        ),
        
        # Row for the table placeholder
        dbc.Row(
            dbc.Col(
                html.Div(
                    "Table Will Go Here",
                    id="patient_table",  # ID for table placeholder
                    className="text-center",
                    style={"fontSize": "26px", "color": "#666", "padding": "50px 0", "fontWeight": "bold"}  # Larger font size for placeholder text
                ),
                width=12,
                style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
            ),
        ),
    ],
    fluid=True,
    style={"padding": "20px", "backgroundColor": "#f8f9fa"}
)


        