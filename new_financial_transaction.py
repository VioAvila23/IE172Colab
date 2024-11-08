from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Input, Output, State
from app import app
from apps.dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate

layout = html.Div(
    [
        dcc.Store(id='financial_transaction_id', storage_type='memory', data=0),
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

                # Treatment Name
                dbc.Row(
                    [
                        dbc.Label("Treatment Name", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='treatment_name_dropdown',
                                placeholder='Select Treatment Name',
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),
                
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
                                options=[
                                {'label': 'Paid', 'value': 'Paid'},
                                {'label': 'Partially Paid', 'value': 'Partially_Paid'},
                                {'label': 'Not Paid', 'value': 'Not_Paid'}
                                ],
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
                ),

                # Mark for Deletion
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
                )
            ]
        ),
        dbc.Alert(id='submit_alert', is_open=False)
    ],
    className="container mt-4"
)

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


@app.callback(
    Output('treatment_name_dropdown', 'options'),
    Input('treatment_name_dropdown', 'id')
)
def load_treatment_names(_):
    # SQL query to fetch treatment names
    sql = """
        SELECT treatment_id, treatment_m AS treatment_name
        FROM treatment
    """
    # Fetch data from DB with empty values and columns lists
    df = getDataFromDB(sql, [], ["treatment_id", "treatment_name"])
    
    # Return data as options for dropdown
    return [{"label": row["treatment_name"], "value": row["treatment_id"]} for _, row in df.iterrows()]

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

# @app.callback(
#     [Output('submit_alert', 'color'),
#      Output('submit_alert', 'children'),
#      Output('submit_alert', 'is_open')],
#     [Input('submit_button', 'n_clicks')],
#     [State('patient_name_dropdown', 'value'),
#      State('treatment_name_dropdown', 'value'),
#      State('financialtransaction_date', 'value'),
#      State('financialtransaction_paymentamount', 'value'),
#      State('financialtrasaction_status', 'value'),
#      State('financialtransaction_paidamount', 'value'),
#      State('financialtransaction_remarks', 'value'),
#      State('url', 'search'),
#      State('financial_transaction_id', 'data')]
# )
# def submit_form(n_clicks, patient_name_dropdown, treatment_name_dropdown, financialtransaction_date, 
#                 financialtransaction_paymentamount, financialtrasaction_status, financialtransaction_paidamount,
#                 financialtransaction_remarks, urlsearch, financial_transaction_id):
    
#     ctx = dash.callback_context
#     if not ctx.triggered or not n_clicks:
#         raise PreventUpdate

#     parsed = urlparse(urlsearch)
#     create_mode = parse_qs(parsed.query).get('mode', [''])[0]

#     # Check for missing values in the required fields
#     if not all([patient_name_dropdown, treatment_name_dropdown, financialtransaction_date,
#                 financialtransaction_paymentamount, financialtrasaction_status, financialtransaction_paidamount,
#                 financialtransaction_remarks]):
#         return 'danger', 'Please fill in all required fields.', True

    # # SQL to insert or update the database
    # if create_mode == 'add':
    #     sql = """INSERT INTO patient (patient_last_m, patient_first_m, patient_middle_m, patient_bd, age,
    #             sex, patient_cn, patient_email, street, barangay, city, postal_code, account_creation_date)
    #             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE);"""
        
    #     values = [last_name, first_name, middle_name, birthdate, age, sex, cellphone_number, 
    #               email_address, street, barangay, city, postal_code]
    
    # elif create_mode == 'edit':
    #     sql = """UPDATE patient
    #             SET patient_last_m = %s,
    #                 patient_first_m = %s,
    #                 patient_middle_m = %s,
    #                 patient_bd = %s,
    #                 age = %s,
    #                 sex = %s,
    #                 patient_cn = %s,
    #                 patient_email = %s,
    #                 street = %s,
    #                 barangay = %s,
    #                 city = %s,
    #                 postal_code = %s
    #             WHERE patient_id = %s;"""
        
    #     values = [last_name, first_name, middle_name, birthdate, age, sex, cellphone_number, 
    #               email_address, street, barangay, city, postal_code, patientprofile_id]
    # else:
    #     raise PreventUpdate

    # try:
    #     modifyDB(sql, values)
    #     return 'success', 'Patient Profile Submitted successfully!', True
    # except Exception as e:
    #     return 'danger', f'Error Occurred: {e}', True
