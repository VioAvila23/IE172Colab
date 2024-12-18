import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([
    # Title Row for Patient Profile Management
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Patient Profile Management', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Patient",
                    href='/patient_profile/patient_management_profile?mode=add',
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

    # Row for search bar and Add New Patient button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Patient ID or Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_patient_name",  # ID for search bar
                        type="text",
                        placeholder="Enter patient ID or name...",
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

    # Row for the table placeholder
    dbc.Row(
        dbc.Col(
            html.Div(
                id="patient-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1000px"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('patient-table', 'children'),
    [
        Input('search_patient_name', 'value'),
    ]
)
def update_records_table(patientfilter):
    # Base SQL query for the Patient table
    sql = """
        SELECT 
            p.patient_id,
            CONCAT(p.patient_last_m, ', ', p.patient_first_m, ' ', COALESCE(p.patient_middle_m, '')) AS "Patient Name",
            p.age AS "Age",
            p.patient_cn AS "Patient Contact Number",
            p.patient_email AS "Patient Email Address",
            MAX(CASE WHEN a.appointment_status = 'Completed' THEN TO_CHAR(a.appointment_date, 'DD, Month, YYYY') ELSE NULL END) AS "Last Visit"
        FROM 
            Patient p
        LEFT JOIN 
            Appointment a ON p.patient_id = a.patient_id
        WHERE 
            p.patient_delete = FALSE
    """
    val = []

    # Add additional filtering conditions if a filter is provided
    if patientfilter:
        # Check if the filter is numeric to search by patient_id
        if patientfilter.isdigit():
            sql += " AND p.patient_id = %s"
            val.append(int(patientfilter))
        else:
            sql += """
                AND (
                    p.patient_last_m ILIKE %s OR 
                    p.patient_first_m ILIKE %s OR 
                    p.patient_middle_m ILIKE %s
                )
            """
            val.extend([f'%{patientfilter}%'] * 3)

    # Add the GROUP BY and ORDER BY clauses
    sql += """
        GROUP BY 
            p.patient_id, p.patient_last_m, p.patient_first_m, p.patient_middle_m, p.age, p.patient_cn, p.patient_email
        ORDER BY 
            p.patient_id
    """

    # Define the column names
    col = ["Patient ID", "Patient Name", "Age", "Patient Contact Number", "Patient Email Address", "Last Visit"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each patient
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/patient_profile/patient_management_profile?mode=edit&id={row["Patient ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]
    display_columns = ["Patient Name", "Age", "Patient Contact Number", "Patient Email Address", "Last Visit", "Action"]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
