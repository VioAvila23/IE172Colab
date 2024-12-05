import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from apps.dbconnect import getDataFromDB
from app import app

# Layout definition
layout = html.Div(
    style={
        'backgroundColor': '#FFF',
        'minHeight': '60vh',
        'margin': '0px',
        'padding': '0px',
        'display': 'flex',
        'flexDirection': 'column'
    },
    children=[
        dbc.Container(
            [
                # Section for filter and buttons
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                # Filter and Buttons Row
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="year-filter",
                                                options=[
                                                    {"label": str(year), "value": year}
                                                    for year in range(2010, 2024)
                                                ],
                                                placeholder="Select Year",
                                                style={
                                                    "width": "100%",
                                                    "borderRadius": "8px",
                                                    "padding": "10px"
                                                }
                                            ),
                                            width=3,
                                            style={"marginRight": "10px"}
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Patients per Month",
                                                id="btn-patients-month",
                                                className="me-2",
                                                style={
                                                    'backgroundColor': '#194D62',
                                                    'color': 'white',
                                                    'padding': '10px 20px',
                                                    'width': '100%',
                                                    'borderRadius': '12px'
                                                }
                                            ),
                                            width=3,
                                            style={'marginRight': '10px'}
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Treatments per Month",
                                                id="btn-treatments-month",
                                                style={
                                                    'backgroundColor': '#194D62',
                                                    'color': 'white',
                                                    'padding': '10px 20px',
                                                    'width': '100%',
                                                    'borderRadius': '12px',
                                                }
                                            ),
                                            width=3
                                        ),
                                    ],
                                    justify="center",
                                    align="center",
                                    style={
                                        "padding": "10px",
                                        "margin": "0"
                                    }
                                ),
                            ],
                            style={
                                'border': '2px solid #194D62',
                                'borderRadius': '10px',
                                'padding': '20px',
                                'backgroundColor': '#F8F9FA',
                                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'width': '100%',
                            }
                        )
                    )
                ),
                # Row for table and graph
                dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="patients_per_month_graph",
                                    style={
                                        'height': '60vh',
                                        'margin': 'auto',  # Center horizontally
                                        'padding': '10px'
                                    },
                                ),
                                width=6,
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'center',  # Center horizontally
                                    'alignItems': 'center'  # Center vertically
                                }
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="treatments_per_month_graph",
                                    style={
                                        'height': '60vh',
                                        'margin': 'auto',  # Center horizontally
                                        'padding': '10px'
                                    },
                                ),
                                width=6,
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'center',  # Center horizontally
                                    'alignItems': 'center'  # Center vertically
                                }
                            ),
                        ],
                        style={
                            'margin': '30px',
                            'width': '100%',
                            'display': 'flex',
                            'justifyContent': 'center'  # Center the entire row
                        }
                    )
            ],
            fluid=True,
            style={'padding': '0px', 'flexGrow': '1'}
        ),
    ]
)

# Callback to update the table and graph based on the button clicked
@app.callback(
    [Output('patients_per_month_graph', 'figure'),
     Output('treatments_per_month_graph', 'figure')],
    [Input('btn-patients-month', 'n_clicks'),
     Input('btn-treatments-month', 'n_clicks'),
     Input('year-filter', 'value')]
)
def update_clinic_graphs(btn_patients_month, btn_treatments_month, selected_year):
    # Determine the context of the button clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    year_filter_condition = f"AND EXTRACT(YEAR FROM appointment_date) = {selected_year}" if selected_year else ""

    patients_sql = f"""
    SELECT 
        TO_CHAR(appointment_date, 'YYYY-MM') AS Month,
        COUNT(DISTINCT patient_id) AS PatientCount
    FROM Appointment
    WHERE 
        appointment_status = 'Completed' 
        AND NOT appointment_delete
        {year_filter_condition}
    GROUP BY TO_CHAR(appointment_date, 'YYYY-MM')
    ORDER BY TO_CHAR(appointment_date, 'YYYY-MM');
    """

    treatments_sql = f"""
    SELECT 
        TO_CHAR(a.appointment_date, 'YYYY-MM') AS Month,
        t.treatment_m AS TreatmentName,
        SUM(at.quantity) AS TreatmentCount
    FROM Appointment_treatment at
    INNER JOIN Appointment a ON at.appointment_id = a.appointment_id
    INNER JOIN Treatment t ON at.treatment_id = t.treatment_id
    WHERE 
        a.appointment_status = 'Completed' 
        AND NOT a.appointment_delete 
        AND NOT at.appointment_treatment_delete 
        AND NOT t.treatment_delete
        {year_filter_condition}
    GROUP BY TO_CHAR(a.appointment_date, 'YYYY-MM'), t.treatment_m
    ORDER BY TO_CHAR(a.appointment_date, 'YYYY-MM'), t.treatment_m;
    """

    patients_data = getDataFromDB(patients_sql, [], ["Month", "PatientCount"])
    treatments_data = getDataFromDB(treatments_sql, [], ["Month", "Treatment Name", "TreatmentCount"])

    fig_patients, fig_treatments = {}, {}

    if button_id == "btn-patients-month":
        fig_patients = px.bar(
            patients_data,
            x="Month",
            y="PatientCount",
            title="Patients per Month",
            labels={"Month": "Month", "PatientCount": "Number of Patients"}
        )
    elif button_id == "btn-treatments-month":
        fig_treatments = px.bar(
            treatments_data,
            x="Month",
            y="TreatmentCount",
            color="Treatment Name",
            title="Treatments per Month",
            labels={"Month": "Month", "TreatmentCount": "Number of Treatments", "Treatment Name": "Treatment Type"}
        )

    return fig_patients, fig_treatments