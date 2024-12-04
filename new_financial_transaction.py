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
                        dbc.Col(
                            dbc.Button(
                                "Generate Transaction",
                                id='generate_transaction_button',
                                color="primary",
                                className="mt-0",
                                style={
                                    "borderRadius": "20px",
                                    "fontWeight": "bold",
                                    "fontSize": "18px",
                                    "backgroundColor": "#194D62",
                                    "color": "white",
                                    "marginLeft": "10px"
                                },
                                n_clicks=0
                            ),
                            width="auto"
                        )
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

        # Alert for submission
        dbc.Alert(id='submit_alert', is_open=False)
    ],
    fluid=True,  # Use dbc.Container's fluid attribute
    style={"padding": "20px", "backgroundColor": "#f8f9fa"}
)


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

#Generate Transaction Table

@app.callback(
    [Output('financial_record_table', 'children'),
     Output('payment_total','children')],
    [Input('generate_transaction_button', 'n_clicks')],
    [State('medical_appointment', 'value')]
)

def generate_transactions(n_clicks,choice):

   #Generates Receipt
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

    return table, total_payment




