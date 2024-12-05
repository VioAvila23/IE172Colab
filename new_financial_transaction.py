import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Input, Output, State
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
from urllib.parse import parse_qs, urlparse


layout = dbc.Container(
    [
        dcc.Store(id='financial_transaction_id', storage_type='memory', data=0),
        dcc.Store(id='financial_transaction_edit_id', storage_type='memory', data=0),

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
                # Select Recently Completed Appointment with Generate Button
                dbc.Row(
                    [
                        dbc.Label(
                            "Select Recently Completed Appointment: ",
                            style={"fontSize": "20px", "fontWeight": "bold"}
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='medical_appointment',
                                placeholder='Select Appointment',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                        
                    ],
                    className="mb-3",
                    id='appointment_dropdown_row'
                ),

                # Row for the medical records table placeholder
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            id="financial_record_table",  # ID for medical records table placeholder
                            className="text-center",
                            style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "300px"}  # Adjust height here
                        ),
                        width=12,
                        style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px", "marginBottom": "20px"}
                    )
                ),
                

                # Total Amount to Be Paid
                dbc.Row(
                    [
                        dbc.Label("Payment Total: ", width=2),
                        dbc.Col(
                            html.Div(
                                id='payment_total',
                                style={"fontSize": "18px", "fontWeight": "bold"}
                            ),
                            width=8
                        )
                    ],
                    className="mb-3"
                ),
                

                # Payment Amount
                dbc.Row(
                    [
                        dbc.Label("Amount Paid", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_paymentamount',
                                placeholder='Enter Amount Paid',
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
                                    {'label': 'Partially Paid', 'value': 'Partially Paid'},
                                    {'label': 'Not Paid', 'value': 'Not Paid'}
                                ],
                                placeholder='Select Payment Status',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),

                # Remarks
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_remarks',
                                placeholder='Enter Remarks',
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
                    id='financial_transaction_deletediv',
                    className="mb-3"
                ),

                # Submit Button
                dbc.Button(
                    "Submit",
                    id='financial_submit_button',
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

        # Alert for submission
        dbc.Alert(id='financial_submit_alert', is_open=False)
    ],
    fluid=True,  # Use dbc.Container's fluid attribute
    style={"padding": "20px", "backgroundColor": "#f8f9fa"}
)


#Display Dynamic Headers and hides delete id
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

#Populates the Completed Appointment in the Dropdown
@app.callback(
    [Output('medical_appointment', 'options')],
    [Input('financial_transaction_id', 'data')]  # Use the patient ID from the first callback
)
def load_all_completed_appointment(financial_transaction_id):
    if financial_transaction_id >= 0:
        sql = """
            SELECT 
                appointment.appointment_id,
                CONCAT(patient.patient_last_m, ', ', patient.patient_first_m) AS patient_name
            FROM 
                appointment
            JOIN 
                patient ON appointment.patient_id = patient.patient_id
            WHERE 
                appointment.medical_result_id IS NOT NULL
                AND (appointment.payment_id IS NULL OR appointment.payment_id = %s)
                AND appointment.appointment_delete = false
                AND patient.patient_delete = false;
        """
        # Fetch data from the database
        df = getDataFromDB(sql, [0], ["appointment_id", "patient_name"])
        
        # Generate options for the dropdown
        options = [
            {'label': f"Appointment {row['appointment_id']} : {row['patient_name']}", 'value': row['appointment_id']}
            for _, row in df.iterrows()
        ]
        return [options]
    else:
        # Return default message if no financial_transaction_id is provided
        return [[{'label': 'No appointments available', 'value': None}]]

#Generate Transaction Table without button

@app.callback(
    [Output('financial_record_table', 'children'),
     Output('payment_total','children')],
    [Input('medical_appointment', 'value')],
    [State('url', 'search')]
       
)

def generate_transactions(choice,urlsearch):
    #Generates Receipt for Add mode
    
    parsed = urlparse(urlsearch)

    # Get the mode
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Get the payment ID
    payment_id = int(parse_qs(parsed.query).get('id', [0])[0])
    
     

    if create_mode =='add':
    
        sql = """
        SELECT 
        
        treatment.treatment_m AS treatment_name,
        appointment_treatment.quantity,
        treatment.treatment_price,
        appointment.medical_result_id
        FROM 
        appointment_treatment
        JOIN 
        appointment ON appointment_treatment.appointment_id = appointment.appointment_id
        JOIN 
        treatment ON appointment_treatment.treatment_id = treatment.treatment_id
        WHERE 
        appointment.appointment_id = %s
        AND appointment.appointment_delete = false
        AND appointment_treatment.appointment_treatment_delete = false
        AND treatment.treatment_delete = false;
        """
        values = [choice]

        col = ["Treatment Name", "Quantity", "Price", "Medical Result ID"]
        df = getDataFromDB(sql,values,col)
        df['Action'] = [
            html.Div(
                dbc.Button("Edit", color='warning', size='sm', 
                        href=f'/medical_records/medical_record_management_profile?mode=edit&id={row["Medical Result ID"]}'
                        ),
                className='text-center'
            ) for idx, row in df.iterrows() 
        ]
        display_columns = ["Treatment Name", "Quantity", "Price", "Action"]
        
        table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

        #Generates Total Payment

        sql2 = """SELECT SUM(appointment_treatment.quantity * treatment.treatment_price) AS total_price
                FROM 
                appointment_treatment
                JOIN 
                appointment ON appointment_treatment.appointment_id = appointment.appointment_id
                JOIN 
                treatment ON appointment_treatment.treatment_id = treatment.treatment_id
                WHERE 
                appointment.appointment_id = %s
                AND appointment.appointment_delete = false
                AND appointment_treatment.appointment_treatment_delete = false
                AND treatment.treatment_delete = false;"""

        values2 = [choice]

        col2 = ["Total_Payment"]
        df2 = getDataFromDB(sql2, values2, col2)

        total_payment = df2.iloc[0]['Total_Payment']
        
    

    elif create_mode == 'edit':
        sql = """
        SELECT treatment.treatment_m AS treatment_name, appointment_treatment.quantity, treatment.treatment_price
        FROM 
        appointment_treatment
        JOIN 
        appointment ON appointment_treatment.appointment_id = appointment.appointment_id
        JOIN 
        treatment ON appointment_treatment.treatment_id = treatment.treatment_id
        WHERE 
        appointment.payment_id = %s
        AND appointment.appointment_delete = false
        AND appointment_treatment.appointment_treatment_delete = false
        AND treatment.treatment_delete = false;

        """
        values = [payment_id]

        col = ["Treatment Name", "Quantity", "Price"]
        df = getDataFromDB(sql,values,col)
        
        display_columns = ["Treatment Name", "Quantity", "Price"]
        
        table = dbc.Table.from_dataframe(df[display_columns], striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'})

        #Generates Total Payment

        sql2 =  """SELECT SUM(appointment_treatment.quantity * treatment.treatment_price) AS total_price
                FROM 
                appointment_treatment
                JOIN 
                appointment ON appointment_treatment.appointment_id = appointment.appointment_id
                JOIN 
                treatment ON appointment_treatment.treatment_id = treatment.treatment_id
                WHERE 
                appointment.payment_id = %s
                AND appointment.appointment_delete = false
                AND appointment_treatment.appointment_treatment_delete = false
                AND treatment.treatment_delete = false;"""

        values2 = [payment_id]

        col2 = ["Total_Payment"]
        df2 = getDataFromDB(sql2, values2, col2)

        total_payment = df2.iloc[0]['Total_Payment']
        
    return table, total_payment

#Adds to New Payment to Database
@app.callback(
    [
        Output('financial_submit_alert', 'color'),
        Output('financial_submit_alert', 'children'),
        Output('financial_submit_alert', 'is_open')
    ],
    [Input('financial_submit_button', 'n_clicks')],
    [
        State('medical_appointment', 'value'),
        State('financialtransaction_paymentamount', 'value'),
        State('financialtrasaction_status', 'value'),
        State('financialtransaction_remarks', 'value'),
        State('url', 'search'),
        State('financial_transaction_id', 'data')
        
    ]
)

def financial_submit_form(n_clicks, appointment_id,payment_amount, payment_status, remarks, urlsearch, transaction_id):

    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    if not all([payment_amount, payment_status, remarks, urlsearch]):
        return 'danger', 'Please fill in all required fields.', True

    #Get payment total using SQL
    

    
    
    if create_mode == 'add':
        sqlt = """SELECT SUM(appointment_treatment.quantity * treatment.treatment_price) AS total_price
            FROM 
            appointment_treatment
            JOIN 
            appointment ON appointment_treatment.appointment_id = appointment.appointment_id
            JOIN 
            treatment ON appointment_treatment.treatment_id = treatment.treatment_id
            WHERE 
            appointment.appointment_id = %s
            AND appointment.appointment_delete = false
            AND appointment_treatment.appointment_treatment_delete = false
            AND treatment.treatment_delete = false;"""

        valuest = [appointment_id]

        colt = ["Total_Payment"]
        df2 = getDataFromDB(sqlt, valuest, colt)
        total_payment = int(df2.iloc[0]['Total_Payment'])
        sql = """INSERT INTO Payment (payment_date,payment_amount,
                 payment_status,paid_amount,remarks)
                 
                 VALUES (CURRENT_DATE,%s,%s,%s,%s)"""
        
        values = [total_payment,payment_status,payment_amount,remarks]

        modifyDB(sql,values)


        # SQL to find the max payment_id
        sql_find = """SELECT MAX(payment.payment_id) FROM payment"""
        df_find = getDataFromDB(sql_find, [],['Max Payment ID'])
        result_id = int(df_find.iloc[0,0])

        #Inserts the payment to the corresponding appointment selected

        sql2 = """UPDATE Appointment
                SET payment_id = %s
                WHERE appointment_id = %s;"""
        values2 = [result_id,appointment_id]
        modifyDB(sql2,values2)

        return 'success', 'Medical Result Submitted successfully!', True
    
    elif create_mode == 'edit':
        #Gets total payment
        parsed = urlparse(urlsearch)

        # Get the mode
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        # Get the payment ID
        payment_id = int(parse_qs(parsed.query).get('id', [0])[0])
        sql2 =  """SELECT SUM(appointment_treatment.quantity * treatment.treatment_price) AS total_price
                FROM 
                appointment_treatment
                JOIN 
                appointment ON appointment_treatment.appointment_id = appointment.appointment_id
                JOIN 
                treatment ON appointment_treatment.treatment_id = treatment.treatment_id
                WHERE 
                appointment.payment_id = %s
                AND appointment.appointment_delete = false
                AND appointment_treatment.appointment_treatment_delete = false
                AND treatment.treatment_delete = false;"""

        values2 = [payment_id]

        col2 = ["Total_Payment"]
        df2 = getDataFromDB(sql2, values2, col2)

        total_payment = int(df2.iloc[0]['Total_Payment'])
        
        sql = """UPDATE Payment
                 SET payment_amount = %s,
                     payment_status = %s,
                     paid_amount = %s,
                     remarks = %s
                 WHERE payment_id = %s"""
        values = [total_payment,payment_status,payment_amount,remarks,payment_id]
        modifyDB(sql,values)
    else:
        raise PreventUpdate
    try:
        return'success', 'Patient Profile Submitted successfully!', True
    except Exception as e:
        return 'danger', f'Error Occurred: {e}', True

#this prepopulates during edit mode

@app.callback(
    [
        Output('financialtransaction_paymentamount', 'value'),
        Output('financialtrasaction_status', 'value'),
        Output('financialtransaction_remarks', 'value')
    ],
    [Input('financial_transaction_id', 'modified_timestamp')],
    [State('financial_transaction_id', 'data')]
)
def financial_populate_edit(timestamp, financial_transaction_id):
    if financial_transaction_id > 0:
        # SQL query to fetch financial transaction details
        sql = """
        SELECT 
            paid_amount, 
            payment_status, 
            remarks
        FROM 
            Payment
        WHERE 
            payment_id = %s
        """
        # Parameters for the query
        values = [financial_transaction_id]
        col = ['payment_amount', 'payment_status', 'remarks']

        # Fetch data from the database
        df = getDataFromDB(sql, values, col)

        # Extract values from the DataFrame
        if not df.empty:
            payment_amount = df['payment_amount'][0]
            payment_status = df['payment_status'][0]
            remarks = df['remarks'][0]

            # Return values to populate the fields
            return payment_amount, payment_status, remarks
        else:
            # Handle case where no data is found
            return None, None, None
    else:
        # Prevent update if financial_transaction_id is invalid
        raise PreventUpdate
