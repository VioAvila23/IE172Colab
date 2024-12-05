import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import datetime
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs, urlparse
from dbconnect import getDataFromDB
# Generate a list of years for the dropdown
years = [{"label": str(year), "value": str(year)} for year in range(2000, datetime.datetime.now().year + 1)]



# Generate a list of years for the dropdown
years = [{"label": str(year), "value": str(year)} for year in range(2000, datetime.datetime.now().year + 1)]

layout = dbc.Container(
    [
        # Header Section
        html.Div(
            [
                html.H3("Dental Studio Key Performance Index (KPIs)", className="text-center", style={"fontWeight": "bold"}),
            ],
            className="mb-4",
        ),

        html.Hr(style={"borderTop": "3px solid #000"}),  # Thick divider

        # Monthly Patient Visits Section
        html.Div(
            [
                html.H4("Monthly Patient Visits Count", className="text-center mb-3", style={"fontWeight": "bold"}),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Filter by Year:", style={"fontWeight": "bold", "display": "block"}),
                                dcc.Dropdown(
                                    id="performance_patient_filter_year_id",
                                    options=years,
                                    placeholder="Select Year",
                                    className="form-control",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-3 justify-content-start",
                ),

                html.Div(
                    "No Filter Selected. Please Select Year",
                    id="performance_patient_graph_holder_id",
                    className="text-center border border-secondary rounded p-5",
                    style={"minHeight": "200px"},
                ),
            ],
            className="mb-5",
        ),

        html.Hr(style={"borderTop": "3px solid #000"}),  # Thick divider

        # Monthly Treatment Count Section
        html.Div(
            [
                html.H4("Monthly Treatment Count", className="text-center mb-3", style={"fontWeight": "bold"}),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Filter by Year:", style={"fontWeight": "bold", "display": "block"}),
                                dcc.Dropdown(
                                    id="performance_treatment_filter_year_id",
                                    options=years,
                                    placeholder="Select Year",
                                    className="form-control",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.Label("Filter by Treatment:", style={"fontWeight": "bold", "display": "block"}),
                                dcc.Dropdown(
                                    id="performance_treatment_filter_name_id",
                                    placeholder="Select Treatment Name",
                                    className="form-control",
                                    style={"width": "100%"}
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                html.Div(
                    "No Filter Selected. Please Select Year and Treatment Name",
                    id="performance_treatment_graph_holder_id",
                    className="text-center border border-secondary rounded p-5",
                    style={"minHeight": "200px"},
                ),
            ],
        ),

        html.Hr(style={"borderTop": "3px solid #000"}),  # Final divider
    ],
    fluid=True,
    style={"padding": "20px"},
)
@app.callback(
    Output("performance_treatment_filter_name_id", "options"),
    Input("performance_treatment_filter_name_id", "id")
)
def load_treatment_names(_):
    # SQL query to fetch active treatment names and IDs
    sql = """
        SELECT treatment_id, treatment_m
        FROM Treatment
        WHERE treatment_delete = false;
    """
    # Fetch data from DB
    df = getDataFromDB(sql, [], ["treatment_id", "treatment_m"])
    
    # Convert the data to dropdown options
    return [{"label": row["treatment_m"], "value": row["treatment_id"]} for _, row in df.iterrows()]

import plotly.express as px
from dash import Input, Output
@app.callback(
    Output("performance_patient_graph_holder_id", "children"),
    Input("performance_patient_filter_year_id", "value")
)
def update_patient_visits_graph(selected_year):
    if not selected_year:
        raise PreventUpdate

    # SQL query to fetch monthly patient visits with "Completed" status
    sql = """
        SELECT 
            TO_CHAR(appointment_date, 'Month') AS month_name,
            COUNT(*) AS visit_count
        FROM Appointment
        WHERE appointment_delete = false
          AND appointment_status = 'Completed'
          AND EXTRACT(YEAR FROM appointment_date) = %s
        GROUP BY TO_CHAR(appointment_date, 'Month'), EXTRACT(MONTH FROM appointment_date)
        ORDER BY EXTRACT(MONTH FROM appointment_date);
    """
    # Fetch data from the database
    df = getDataFromDB(sql, [selected_year], ["month_name", "visit_count"])

    if df.empty:
        return html.Div("No data available for the selected year.", className="text-center text-danger")

    # Create a bar graph using Plotly
    fig = px.bar(
        df,
        x="month_name",
        y="visit_count",
        title=f"Monthly Completed Patient Visits for {selected_year}",
        labels={"month_name": "Month", "visit_count": "Number of Patients"},
    )
    fig.update_layout(title_font_size=20, xaxis_title="Month", yaxis_title="Number of Patients")

    return dcc.Graph(figure=fig)

@app.callback(
    Output("performance_treatment_graph_holder_id", "children"),
    [
        Input("performance_treatment_filter_year_id", "value"),
        Input("performance_treatment_filter_name_id", "value"),
    ]
)
def update_treatment_count_graph(selected_year, selected_treatment):
    if not selected_year or not selected_treatment:
        raise PreventUpdate

    # SQL query to fetch monthly treatment counts
    sql = """
        SELECT 
            TO_CHAR(a.appointment_date, 'Month') AS month_name,
            COUNT(*) AS treatment_count
        FROM Appointment_treatment at
        JOIN Appointment a ON at.appointment_id = a.appointment_id
        JOIN Treatment t ON at.treatment_id = t.treatment_id
        WHERE at.appointment_treatment_delete = false
          AND t.treatment_delete = false
          AND a.appointment_delete = false
          AND a.appointment_status = 'Completed'
          AND EXTRACT(YEAR FROM a.appointment_date) = %s
          AND t.treatment_id = %s
        GROUP BY TO_CHAR(a.appointment_date, 'Month'), EXTRACT(MONTH FROM a.appointment_date)
        ORDER BY EXTRACT(MONTH FROM a.appointment_date);
    """
    # Fetch data from the database
    df = getDataFromDB(sql, [selected_year, selected_treatment], ["month_name", "treatment_count"])

    if df.empty:
        return html.Div("No data available for the selected year and treatment.", className="text-center text-danger")

    # Create a bar graph using Plotly
    fig = px.bar(
        df,
        x="month_name",
        y="treatment_count",
        title=f"Monthly Treatment Count for {selected_year}",
        labels={"month_name": "Month", "treatment_count": "Number of Treatments"},
    )
    fig.update_layout(title_font_size=20, xaxis_title="Month", yaxis_title="Number of Treatments")

    return dcc.Graph(figure=fig)


