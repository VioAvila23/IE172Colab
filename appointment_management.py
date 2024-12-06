import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    # Title Row for Appointment Management
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Appointment Management', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Schedule Appointment",
                    href='/appointments/appointment_management_profile?mode=add',
                    style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white", "marginBottom": "0px"},
                    className="float-end"
                ),
                md=4,
                style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
            ),
        ],
        className="mb-1", # Adjust margin-bottom of row
        align="center"
    ),
    html.Hr(),

    # Row for search bar and appointment button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Appointment ID or Patient Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_appointment", 
                        type="text",
                        placeholder="Enter Appointment ID or Patient Name...",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            ),
        ],
        className="mb-4",
        align="center"
    ),

    # Filter by Appointment Status
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Filter by Appointment Status", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Dropdown(
                        id="status_filter",
                        options=[
                            {"label": "Scheduled", "value": "Scheduled"},
                            {"label": "Pending", "value": "Pending"},
                            {"label": "Completed", "value": "Completed"},
                        ],
                        placeholder="Select Appointment Status",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            )
        ],
        className="mb-4",
        align="center"
    ),

    # Table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="appointment-table", 
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1500px"} 
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('appointment-table', 'children'),
    [
        Input('search_appointment', 'value'),
        Input('status_filter', 'value'),
    ]
)
def update_records_table(appointmentfilter, status_filter):
    # Base SQL query with date and time formatting
    sql = """
    SELECT 
        appointment.appointment_id AS "Appointment ID",
        CONCAT(patient.patient_last_m, ', ', patient.patient_first_m) AS "Patient Name",
        appointment.appointment_status AS "Appointment Status", 
        TO_CHAR(appointment.appointment_date, 'DD, Month YYYY') AS "Appointment Date", 
        TO_CHAR(appointment.appointment_time, 'HH12:MI AM') AS "Appointment Time",
        appointment.appointment_reason AS "Appointment Reason"
    FROM 
        appointment
    JOIN 
        patient ON appointment.patient_id = patient.patient_id
    WHERE 
        appointment.appointment_delete = FALSE
    """

    # SQL conditions and values
    conditions = []
    val = []

    # Add conditions based on input values
    if appointmentfilter:
        if appointmentfilter.isdigit():
            conditions.append("appointment.appointment_id = %s")
            val.append(int(appointmentfilter))
        else:
            conditions.append("""
                (patient.patient_last_m ILIKE %s OR 
                 patient.patient_first_m ILIKE %s OR 
                 patient.patient_middle_m ILIKE %s)
            """)
            val.extend([f'%{appointmentfilter}%'] * 3)

    if status_filter:
        conditions.append("appointment.appointment_status = %s")
        val.append(status_filter)

    # Add additional conditions to the WHERE clause
    if conditions:
        sql += " AND " + " AND ".join(conditions)

    # Add ORDER BY clause
    sql += """
        ORDER BY 
            appointment.appointment_id DESC
    """

    # Define the column names
    col = ["Appointment ID", "Patient Name", "Appointment Status", "Appointment Date", "Appointment Time", "Appointment Reason"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Adding action buttons for each row
    df['Action'] = [
        html.Div(
            dbc.Button(
                "Reschedule", 
                color='warning', 
                size='sm', 
                href=f'/appointments/appointment_management_profile?mode=edit&id={row["Appointment ID"]}'
            ),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Limit columns for display but include the Action column
    display_columns = ["Appointment ID", "Patient Name", "Appointment Status", "Appointment Date", "Appointment Time", "Appointment Reason", "Action"]

    # Create the table from the DataFrame
    table = dbc.Table.from_dataframe(
        df[display_columns], 
        striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'}
    )

    return [table]