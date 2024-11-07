import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    # Row fsor search bar and Add New Patient button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search by Patient ID or Patient Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_medical_records",  # ID for search bar
                        type="text",
                        placeholder="Enter Patient ID or Patient Name",
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

    # Row for the table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="medical_record_table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1000px"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('medical_record_table', 'children'),
    [
    Input('search_medical_records', 'value'),
    ]
)
def update_records_table(patientfilter):
    # Base SQL query for the Patient table with only Patient ID and Patient Name
    sql = """
        SELECT 
        p.patient_id,
        CONCAT(p.patient_last_m, ', ', p.patient_first_m, ' ', COALESCE(p.patient_middle_m, '')) AS "Patient Name"
        FROM 
        Patient p
        LEFT JOIN 
        Appointment a ON p.patient_id = a.patient_id
    """
    val = []

    # Add the WHERE clause if a filter is provided
    if patientfilter:
        # Check if the filter is numeric to search by patient_id
        if patientfilter.isdigit():
            sql += " WHERE p.patient_id = %s"
            val.append(int(patientfilter))
        else:
            sql += """
                WHERE 
                p.patient_last_m ILIKE %s OR 
                p.patient_first_m ILIKE %s OR 
                p.patient_middle_m ILIKE %s
            """
            val.extend([f'%{patientfilter}%'] * 3)

    # Add the GROUP BY and ORDER BY clauses for Patient ID and Patient Name
    sql += """
        GROUP BY 
        p.patient_id, p.patient_last_m, p.patient_first_m, p.patient_middle_m
        ORDER BY 
        p.patient_id
    """

    # Define the column names for the resulting DataFrame
    col = ["Patient ID", "Patient Name"]


    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each patient
    df['View Medical Record'] = [
        html.Div(
            dbc.Button("View", color='warning', size='sm', 
                       href=f'/medical_records/medical_record_profile?mode=view&id={row["Patient ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
