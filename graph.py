import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from apps.dbconnect import getDataFromDB
from app import app

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
                # Section for filters and buttons
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
                                            dcc.Dropdown(
                                                id="treatment-name-filter",
                                                options=[],  # Populated dynamically
                                                placeholder="Select Treatment",
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
                                            width=2,
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
                                            width=2
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
                                        'margin': 'auto',
                                        'padding': '10px'
                                    },
                                ),
                                width=6,
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center'
                                }
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="treatments_per_month_graph",
                                    style={
                                        'height': '60vh',
                                        'margin': 'auto',
                                        'padding': '10px'
                                    },
                                ),
                                width=6,
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center'
                                }
                            ),
                        ],
                        style={
                            'margin': '30px',
                            'width': '100%',
                            'display': 'flex',
                            'justifyContent': 'center'
                        }
                    )
            ],
            fluid=True,
            style={'padding': '0px', 'flexGrow': '1'}
        ),
    ]
)

@app.callback(
    Output('treatment-name-filter', 'options'),
    Input('year-filter', 'value')
)
def populate_treatment_names(selected_year):
    year_filter_condition = f"WHERE EXTRACT(YEAR FROM appointment_date) = {selected_year}" if selected_year else ""
    treatments_sql = f"""
    SELECT DISTINCT t.treatment_m AS TreatmentName
    FROM Treatment t
    INNER JOIN Appointment_treatment at ON t.treatment_id = at.treatment_id
    INNER JOIN Appointment a ON at.appointment_id = a.appointment_id
    WHERE NOT t.treatment_delete 
      AND NOT at.appointment_treatment_delete
      AND NOT a.appointment_delete
      {year_filter_condition};
    """
    treatments_data = getDataFromDB(treatments_sql, [], ["TreatmentName"])
    return [{"label": name, "value": name} for name in treatments_data["TreatmentName"]]


@app.callback(
    [Output('patients_per_month_graph', 'figure'),
     Output('treatments_per_month_graph', 'figure')],
    [Input('btn-patients-month', 'n_clicks'),
     Input('btn-treatments-month', 'n_clicks'),
     Input('year-filter', 'value'),
     Input('treatment-name-filter', 'value')]
)
def update_clinic_graphs(btn_patients_month, btn_treatments_month, selected_year, selected_treatment):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    year_filter_condition = f"AND EXTRACT(YEAR FROM a.appointment_date) = {selected_year}" if selected_year else ""
    treatment_filter_condition = f"AND t.treatment_m = '{selected_treatment}'" if selected_treatment else ""

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
        {treatment_filter_condition}
    GROUP BY TO_CHAR(a.appointment_date, 'YYYY-MM'), t.treatment_m
    ORDER BY TO_CHAR(a.appointment_date, 'YYYY-MM'), t.treatment_m;
    """

    treatments_data = getDataFromDB(treatments_sql, [], ["Month", "TreatmentName", "TreatmentCount"])
    fig_treatments = px.bar(
        treatments_data,
        x="Month",
        y="TreatmentCount",
        color="TreatmentName",
        title="Treatments per Month",
        labels={"Month": "Month", "TreatmentCount": "Number of Treatments", "TreatmentName": "Treatment Type"}
    ) if button_id == "btn-treatments-month" else {}

    return {}, fig_treatments
