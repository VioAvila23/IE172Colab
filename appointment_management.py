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
                        "Filter by Appointment ID, Patient ID, Appointment Date, etc,", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_appointment", 
                        type="text",
                        placeholder="Enter Appointment ID, Patient ID, Appointment Date, etc...",
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
        dbc.Col(
            html.Div(
                id="appointment-table", 
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "500px"} 
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('appointment-table', 'children'),
    [
        Input('search_patient_name', 'value'),
    ]
)
def update_records_table(appointmentfilter):
    sql = """
        SELECT appointment.appointment_id, patient.patient_id, patient.patient_last_m, appointment.appointment_status, appointment.appointment_time, appointment.appointment_date, appointment.appointment_reason

        FROM patient"""
    val = []

    if appointmentfilter:
        sql += " AND patient_name ILIKE %s"
        val.append(f'%{patientfilter}%')

    # Define the column names
    col = ["Appointment ID", "Patient ID", "Patient Name", "Appointment Status", "Appointment Time", "Appointment Date", "Appointment Reason"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    df['Action'] = [
        html.Div(
            dbc.Button("Reschedule", color='warning', size='sm', 
                       href=f'/appointments/appointment_management_profile?mode=edit&id={row["Appointment ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
