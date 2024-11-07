import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from apps.dbconnect import getDataFromDB
from app import app
from dash.exceptions import PreventUpdate

layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Financial Transaction Management', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Financial Transaction",
                    href='/financial_transaction_management/new_transaction?mode=add',
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
    # Row for search bar and Add New Financial Transaction button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Filter by Transaction ID or Patient Name", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_financial_transaction",  # ID for search bar
                        type="text",
                        placeholder="Enter Transaction ID or Patient Name...",
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

    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Filter by Payment Status", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Dropdown(
                        id="status_filter",  # ID for dropdown filter
                        options=[
                            {"label": "Paid", "value": "Paid"},
                            {"label": "Partially Paid", "value": "Partially Paid"},
                            {"label": "Not Paid", "value": "Not Paid"},
                        ],
                        placeholder="Select Payment Status",
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
                id="financialtransaction-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1000px"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('financialtransaction-table', 'children'),
    [
        Input('search_financial_transaction', 'value'),
        Input('status_filter', 'value')
    ]
)
def update_records_table(financial_transaction_filter, status_filter):
    # Modified SQL query with columns in the desired order
    sql = """
        SELECT 
            payment.payment_id AS "Transaction ID", 
            CONCAT(patient.patient_last_m, ', ', patient.patient_first_m) AS "Patient Name", 
            treatment.treatment_m AS "Treatment Name",
            payment.payment_date AS "Payment Date", 
            payment.payment_amount AS "Payment Amount", 
            payment.payment_status AS "Payment Status", 
            payment.paid_amount AS "Paid Amount", 
            payment.remarks AS "Remarks"
        FROM 
            payment
        JOIN 
            appointment_treatment ON payment.payment_id = appointment_treatment.payment_id
        JOIN 
            appointment ON appointment_treatment.appointment_id = appointment.appointment_id
        JOIN 
            patient ON appointment.patient_id = patient.patient_id
        JOIN 
            treatment ON appointment_treatment.treatment_id = treatment.treatment_id
    """
    val = []

    # Constructing the WHERE clause based on search and dropdown filters
    filters = []
    if financial_transaction_filter:
        # Check if the filter is numeric to search by payment_id
        if financial_transaction_filter.isdigit():
            filters.append("payment.payment_id = %s")
            val.append(int(financial_transaction_filter))
        else:
            sql += """
                WHERE 
                patient.patient_last_m ILIKE %s OR 
                patient.patient_first_m ILIKE %s OR 
                patient.patient_middle_m ILIKE %s
            """
            val.extend([f'%{financial_transaction_filter}%'] * 3)
        
    if status_filter:
        filters.append("payment.payment_status = %s")
        val.append(status_filter)

    # Add WHERE clause if any filters are applied
    if filters:
        sql += " WHERE " + " AND ".join(filters)

    # Add the GROUP BY and ORDER BY clauses
    sql += """
        GROUP BY 
        payment.payment_id, patient.patient_last_m, patient.patient_first_m, treatment.treatment_m, 
        payment.payment_date, payment.payment_amount, payment.payment_status, payment.paid_amount, payment.remarks
        ORDER BY 
        payment.payment_id
    """

    # Define the column names in the desired order
    col = ["Transaction ID", "Patient Name", "Treatment Name", "Payment Date", "Payment Amount", "Payment Status", "Paid Amount", "Remarks"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each payment_transaction
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/financial_transaction_management/new_transaction?mode=edit&id={row["Transaction ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
