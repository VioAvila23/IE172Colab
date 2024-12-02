import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Input, Output, State
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
from urllib.parse import parse_qs, urlparse


layout = html.Div(
    [
        dcc.Store(id='financial_transaction_id', storage_type='memory', data=0),
        dcc.Store(id='dropdown-counter', storage_type='memory', data=0),  # Store the number of dynamic dropdowns

        # Header with dynamic title based on mode
        dbc.Row(
            [
                dbc.Col(
                    html.H2(
                        id="financial_transaction_header",
                        style={'font-size': '25px'}
                    ),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/financial_transaction",
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "marginRight": "10px",
                            "backgroundColor": "#194D62"
                        }
                    ),
                    width="auto"
                ),
            ],
            align="center",
            className="mb-4"
        ),
        
        html.Hr(),

        # Form Layout
        dbc.Form(
            [
                # Patient Name
                dbc.Row(
                    [
                        dbc.Label("Patient Name", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='patient_name_dropdown',
                                placeholder='Select Patient Name',
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),

                # Dynamic Dropdowns container (start without the first dropdown)
                html.Div(id='dropdown-container', children=[]),

                # Button to add new dropdowns
                dbc.Button("Add Treatment Done", id="add-dropdown-button",color="primary", 
                    className="mt-3",
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    }, n_clicks=0),

                # Payment Date
                dbc.Row(
                    [
                        dbc.Label("Payment Date", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='financialtransaction_date',
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8, 
                        ),
                    ],
                    className='mb-3'
                ),

                # Payment Amount
                dbc.Row(
                    [
                        dbc.Label("Payment Amount", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_paymentamount',
                                placeholder='Enter Payment Amount',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Payment Status
                dbc.Row(
                    [
                        dbc.Label("Payment Status", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='financialtrasaction_status',
                                options=[{'label': 'Paid', 'value': 'Paid'},
                                         {'label': 'Partially Paid', 'value': 'Partially_Paid'},
                                         {'label': 'Not Paid', 'value': 'Not_Paid'}],
                                placeholder='Payment Status',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),

                # Paid Amount
                dbc.Row(
                    [
                        dbc.Label("Paid Amount", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_paidamount',
                                placeholder='Enter Paid Amount',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Remarks
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_remarks',
                                placeholder='Remarks',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ), # Mark for Deletion
                html.Div(
                    [
                        dbc.Checklist(
                            id='financial_transaction_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='financial_transaction_deletediv'
                ),

                # Submit Button
                dbc.Button(
                    "Submit",
                    id='submit_button',
                    color="primary", 
                    className="mt-3",
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                    n_clicks=0,
                ),
            ]
        ),
        dbc.Alert(id='submit_alert', is_open=False)
    ],
    className="container mt-4"
)

#Display Patient Names
@app.callback(
    Output('patient_name_dropdown', 'options'),
    Input('patient_name_dropdown', 'id')
)
def load_patient_names(_):
    # SQL query to fetch patient names
    sql = """
        SELECT patient_id, CONCAT(patient_last_m, ', ', patient_first_m) AS patient_name
        FROM patient
    """
    # Fetch data from DB with empty values and columns lists
    df = getDataFromDB(sql, [], ["patient_id", "patient_name"])
    
    # Return data as options for dropdown
    return [{"label": row["patient_name"], "value": row["patient_id"]} for _, row in df.iterrows()]


# Callback to handle dynamic dropdowns and display the count and IDs
@app.callback(
    [Output('dropdown-container', 'children'),
     Output('dropdown-counter', 'data')],  # Remove output for dropdown info
    [Input('add-dropdown-button', 'n_clicks')],
    [State('dropdown-container', 'children'),
     State('dropdown-counter', 'data')]  # Get the current count of dropdowns
)
def add_dropdown(n_clicks, current_children, dropdown_count):
    # Prevent update if no click
    if n_clicks == 0:
        raise PreventUpdate

    # Increment the dropdown count
    dropdown_count += 1

    # SQL query to fetch treatment names
    sql = """
        SELECT treatment_id, treatment_m AS treatment_name
        FROM treatment
    """
    # Fetch data from DB
    df = getDataFromDB(sql, [], ["treatment_id", "treatment_name"])

    # Create options for the dropdown based on fetched treatment names
    treatment_options = [
        {"label": row["treatment_name"], "value": row["treatment_id"]}
        for _, row in df.iterrows()
    ]

    # Create a label for the treatment dropdown (Treatment Name 1, Treatment Name 2, etc.)
    treatment_label = f"Treatment Name {dropdown_count}"

    # Create a new row for the dropdown with its label and the actual dropdown
    new_row = dbc.Row(
        [
            dbc.Label(treatment_label, width=2),
            dbc.Col(
                dcc.Dropdown(
                    id={'type': 'dynamic-dropdown', 'index': dropdown_count},  # Unique ID for each dropdown
                    options=treatment_options,  # Use the fetched options
                    placeholder="Select Treatment Name",
                    style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                ),
                width=8,
            ),
        ],
        className='mb-3'
    )

    # Append the new row to the current children
    current_children.append(new_row)

    return current_children, dropdown_count

#Display Dynamic Headers
@app.callback(
    [
        Output('financial_transaction_id', 'data'),
        Output('financial_transaction_deletediv', 'className'),
        Output('financial_transaction_header', 'children')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def financial_transaction_load(pathname, urlsearch):
    if pathname == '/financial_transaction_management/new_transaction':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            financial_transaction_id = 0
            financial_transaction_deletediv = 'd-none'
            header_text = "Add New Financial Transaction Record"
        else:
            financial_transaction_id = int(parse_qs(parsed.query).get('id', [0])[0])
            financial_transaction_deletediv = ''
            header_text = "Edit Financial Transaction Record"
        
        return [financial_transaction_id, financial_transaction_deletediv, header_text]
    else:
        raise PreventUpdate





