import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
from dbconnect import getDataFromDB
from app import app

layout = dbc.Container([  
    # Title Row for Treatment Management
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2(
                        'Treatment Management', 
                        style={"marginBottom": "0px"}  # Reduce space below heading
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                dbc.Button(
                    "Add New Treatment",
                    href='/treatment/treatment_management_profile?mode=add',
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

    # Row for search bar and Add New Treatment button
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(
                        "Search Treatment Name or ID", 
                        className="form-label", 
                        style={"fontSize": "18px", "fontWeight": "bold"}
                    ),
                    dcc.Input(
                        id="search_treatment_name",  # ID for search bar
                        type="text",
                        placeholder="Enter treatment name or ID...",
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
                id="treatment-table",  # ID for table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1000px"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

@app.callback(
    Output('treatment-table', 'children'),
    [
        Input('search_treatment_name', 'value'),
    ]
)
def update_records_table(treatmentfilter):
    # Base SQL query for the Treatment table
    sql = """
        SELECT 
        t.treatment_id,
        t.treatment_m AS "Treatment Name",
        t.treatment_description AS "Description",
        t.treatment_price AS "Price"
        FROM 
        Treatment t
        WHERE
        t.treatment_delete = false
    """
    val = []

    # Add the WHERE clause if a filter is provided
    if treatmentfilter:
        # Check if the filter is numeric to search by treatment_id
        if treatmentfilter.isdigit():
            sql += " AND t.treatment_id = %s"
            val.append(int(treatmentfilter))
        else:
            sql += """
                AND 
                t.treatment_m ILIKE %s OR 
                t.treatment_description ILIKE %s
            """
            val.extend([f'%{treatmentfilter}%', f'%{treatmentfilter}%'])

    # Fetch the filtered data into a DataFrame
    col = ["Treatment ID", "Treatment Name", "Description", "Price"]
    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Format the Price column with PHP and two decimal places
    df['Price'] = df['Price'].apply(lambda x: f"PHP {x:,.2f}")

    # Generating edit buttons for each treatment
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/treatment/treatment_management_profile?mode=edit&id={row["Treatment ID"]}'),
            className='text-center'
        ) for idx, row in df.iterrows()
    ]

    # Creating the updated table with centered text
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

    return [table]
