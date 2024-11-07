import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    
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
            dbc.Col(
                dbc.Button(
                    "Schedule Appointment",
                    href='/appointments/appointment_management_profile?mode=add',
                    style={"borderRadius": "20px", "fontWeight": "bold", "fontSize": "18px", "backgroundColor": "#194D62", "color": "white"},
                    className="float-end"
                ),
                md=4,
                style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"},
            ),
        ],
        className="mb-4",
        align="center"
    ),

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
                        id="status_filter",  # ID for dropdown filter
                        options=[
                            {"label": "Booked", "value": "Booked"},
                            {"label": "Pending", "value": "Pending"},
                            {"label": "Complete", "value": "Complete"},
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
    # Base SQL query
    sql = """
    SELECT 
        appointment.appointment_id AS "Appointment ID",
         
        CONCAT(patient.patient_last_m, ', ', patient.patient_first_m) AS "Patient Name",
        appointment.appointment_status AS "Appointment Status", 
        appointment.appointment_time AS "Appointment Time", 
        appointment.appointment_date AS "Appointment Date", 
        appointment.appointment_reason AS "Appointment Reason"
    FROM 
        appointment
    JOIN 
        appointment_treatment ON appointment.appointment_id = appointment_treatment.appointment_id
    JOIN 
        patient ON appointment.patient_id = patient.patient_id
    JOIN 
        payment ON payment.payment_id = appointment_treatment.payment_id
    JOIN 
        treatment ON appointment_treatment.treatment_id = treatment.treatment_id
    """

    # List to hold SQL conditions and values
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

    # Add WHERE clause if there are conditions
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # Add GROUP BY and ORDER BY clauses
    sql += """
        GROUP BY 
            appointment.appointment_id,  patient.patient_last_m, 
            patient.patient_first_m, appointment.appointment_status, 
            appointment.appointment_time, appointment.appointment_date, appointment.appointment_reason
        ORDER BY 
            appointment.appointment_id DESC
    """

    # Define the column names
    col = ["Appointment ID", "Patient Name", "Appointment Status", "Appointment Time", "Appointment Date", "Appointment Reason"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Adding action buttons for each row
    df['Action'] = [
        html.Div(
            dbc.Button("Reschedule", color='warning', size='sm', 
                       href=f'/appointments/appointment_management_profile?mode=edit&id={row["Appointment ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Create the table from the DataFrame
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
