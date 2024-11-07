import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from apps.dbconnect import getDataFromDB
from app import app
from dash.exceptions import PreventUpdate

layout = dbc.Container([
    # Row for search bar and Add New Financial Transaction button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Filter by Transaction ID, Payment Status, etc,", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_financial_transaction",  # ID for search bar
                        type="text",
                        placeholder="Enter Transaction ID, Payment Status, etc...",
                        className="form-control",
                        style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Financial Transaction",
                    href='/financial_transaction_management/new_transaction?mode=add',
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
    ]
)
def update_records_table(financial_transaction_filter):
    # Base SQL query for the Payment table
    sql = """
        SELECT payment.payment_id, payment.payment_date, payment.payment_amount, payment.payment_status, payment.paid_amount, payment.remarks

        FROM payment"""
    val = []

    if financial_transaction_filter:
        sql += " WHERE payment.payment_status ILIKE %s"
        val.append(f'%{financial_transaction_filter}%')

    # Define the column names
    col = ["Payment ID", "Payment Date", "Payment Amount", "Payment Status", "Paid Amount", "Remarks"]

    # Fetch the filtered data into a DataFrame
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Generating edit buttons for each patient
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/financial_transaction_management/new_transaction?mode=edit&id={row["Payment ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
