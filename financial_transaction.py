import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
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
                        style={"borderRadius": "20px", "fontSize": "18px"}  # Removed backgroundColor
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
    sql = """
    SELECT 
        payment.payment_id AS "Transaction ID", 
        CONCAT(patient.patient_last_m, ', ', patient.patient_first_m) AS "Patient Name", 
        STRING_AGG(treatment.treatment_m, ', ') AS "Treatment Name", 
        TO_CHAR(payment.payment_date, 'DD, Month YYYY') AS "Payment Date", 
        payment.payment_amount AS "Payment Amount", 
        payment.payment_status AS "Payment Status", 
        payment.paid_amount AS "Paid Amount", 
        payment.remarks AS "Remarks"
    FROM 
        payment
    JOIN 
        appointment ON payment.payment_id = appointment.payment_id
    JOIN 
        appointment_treatment ON appointment.appointment_id = appointment_treatment.appointment_id
    JOIN 
        treatment ON appointment_treatment.treatment_id = treatment.treatment_id
    JOIN 
        patient ON appointment.patient_id = patient.patient_id
    WHERE 
        payment.payment_delete = FALSE
        AND (treatment.treatment_delete = FALSE OR (treatment.treatment_delete = TRUE AND treatment.treatment_id != 6))
    """
    val = []
    filters = []

    if financial_transaction_filter:
        if financial_transaction_filter.isdigit():
            filters.append("payment.payment_id = %s")
            val.append(int(financial_transaction_filter))
        else:
            filters.append("""
                (patient.patient_last_m ILIKE %s OR 
                patient.patient_first_m ILIKE %s OR 
                patient.patient_middle_m ILIKE %s)
            """)
            val.extend([f'%{financial_transaction_filter}%'] * 3)

    if status_filter:
        filters.append("payment.payment_status = %s")
        val.append(status_filter)

    if filters:
        sql += " AND " + " AND ".join(filters)

    sql += """
        GROUP BY 
            payment.payment_id, 
            patient.patient_last_m, 
            patient.patient_first_m, 
            payment.payment_date, 
            payment.payment_amount, 
            payment.payment_status, 
            payment.paid_amount, 
            payment.remarks
        ORDER BY 
            payment.payment_id
    """

    col = ["Transaction ID", "Patient Name", "Treatment Name", "Payment Date", "Payment Amount", "Payment Status", "Paid Amount", "Remarks"]

    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    df['Payment Amount'] = df['Payment Amount'].apply(lambda x: f"PHP {x:,.2f}")
    df['Paid Amount'] = df['Paid Amount'].apply(lambda x: f"PHP {x:,.2f}")

    df['Action'] = [
        html.Div(
            dbc.Button(
                "Edit", 
                color='warning', 
                size='sm', 
                href=f'/financial_transaction_management/new_transaction?mode=edit&id={row["Transaction ID"]}'
            ),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    df['Receipt'] = [
        html.Div(
            dbc.Button(
                "Generate", 
                size='sm', 
                href=f'/financial_transaction/financial_generate?mode=generate&id={row["Transaction ID"]}',
                style={'backgroundColor': 'blue', 'color': 'white'}
            ),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    display_columns = ["Transaction ID", "Patient Name", "Treatment Name", "Payment Date", "Payment Amount", "Payment Status", "Paid Amount", "Remarks", "Action", 'Receipt']

    table = dbc.Table.from_dataframe(
        df[display_columns], 
        striped=True, 
        bordered=True, 
        hover=True, 
        size='sm', 
        style={'textAlign': 'center'}
    )

    return [table]

