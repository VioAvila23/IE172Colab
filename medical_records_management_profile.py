import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from dash.dependencies import MATCH, ALL
from urllib.parse import parse_qs, urlparse
from dbconnect import getDataFromDB, modifyDB



  # Import your DB connection method

layout = html.Div(
    [
        dcc.Store(id='medicalresult_edit_id', storage_type='memory', data=0),
        dcc.Store(id='medicalpatientprofile_id', storage_type='memory', data=0),
        dcc.Store(id='medicalresult-dropdown-counter', storage_type='memory', data=0),  # Store the number of dynamic dropdowns

        # Header and Back button
        dbc.Row(
            [
                dbc.Col(html.H2("Add New Medical Record", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/medical_records",
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
                # Appointment Dropdown
                dbc.Row(
                    [
                        dbc.Label("Appointment", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='medicalresult_appointment',  # ID for the dropdown
                                placeholder='Select Appointment',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Condition
                dbc.Row(
                    [
                        dbc.Label("Condition", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_condition',
                                placeholder='Enter Condition',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Diagnosis
                dbc.Row(
                    [
                        dbc.Label("Diagnosis", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_diagnosis',
                                placeholder='Enter Diagnosis',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Prescription
                dbc.Row(
                    [
                        dbc.Label("Prescription", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='medicalresult_prescription',
                                placeholder='Enter Prescription',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Dynamic Dropdowns container for Treatments Done
                html.Div(id='medicalresult-dropdown-container', children=[]),

                # Row for buttons to add and remove treatments
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Add Treatment Done", id="medicalresult_add-dropdown-button", color="primary",
                                       className="mt-3",
                                       style={
                                           "borderRadius": "20px",
                                           "fontWeight": "bold",
                                           "fontSize": "18px",
                                           "backgroundColor": "#194D62",
                                           "color": "white"
                                       }, n_clicks=0),
                            width="auto",
                            className="me-2"
                        ),
                        dbc.Col(
                            dbc.Button("Remove Last Treatment", id="medicalresult_remove-dropdown-button", color="danger",
                                       className="mt-3",
                                       style={
                                           "borderRadius": "20px",
                                           "fontWeight": "bold",
                                           "fontSize": "18px",
                                           "backgroundColor": "#c43f3f",
                                           "color": "white"
                                       }, n_clicks=0),
                            width="auto",
                        ),
                    ],
                    justify="start",
                    className="mt-3"
                ),

                html.Div(
                    [
                        dbc.Checklist(
                            id='medicalresult_patient_profile_delete',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='medicalresult_deletediv'
                ),

                # Submit Button
                dbc.Button(
                    "Submit",
                    color="primary",
                    className="mt-3",
                    id='medicalresult_submit_button',
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                )
            ]
        ),

        # Alert for submission feedback
        dbc.Alert(id='medicalresult_submit_alert', is_open=False)
    ],
    className="container mt-4"
)

#Gets patient ID from url
@app.callback(
    [Output('medicalpatientprofile_id', 'data')],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def medical_profile_load(pathname, urlsearch):
    if pathname == '/medical_records/medical_record_management_profile':
        # Parse the URL to extract the patient ID
        parsed = urlparse(urlsearch)
        medicalpatientprofile_id = parse_qs(parsed.query).get('id', [0])[0]
        return [medicalpatientprofile_id]  # Return patient ID to store it in memory
    else:
        raise PreventUpdate
#Puts Appointments without medical result pa sa options for the corresponding patient ID
@app.callback(
    Output('medicalresult_appointment', 'options'),
    [Input('medicalpatientprofile_id', 'data')]  # Use the patient ID from the first callback
)
def load_all_appointments(medicalpatientprofile_id):
    if medicalpatientprofile_id:  # Check if the ID is not None or 0
        # SQL query to fetch appointments specific to the patient ID with proper date and time formatting
        sql = """
            SELECT appointment_id, 
                   TO_CHAR(appointment_date, 'DD, Month, YYYY') AS formatted_date,
                   TO_CHAR(appointment_time, 'HH12:MI AM') AS formatted_time
            FROM appointment
            WHERE patient_id = %s 
              AND (medical_result_id IS NULL OR medical_result_id = 0)  
        """
        # Fetch data from DB
        df = getDataFromDB(sql, [medicalpatientprofile_id], ["appointment_id", "formatted_date", "formatted_time"])

        # Convert the fetched data into options for the dropdown
        return [{'label': f"Appointment ({row['formatted_date']}), {row['formatted_time']}", 'value': row['appointment_id']} for _, row in df.iterrows()]
    else:
        # If no patient ID, return an empty list or a default message
        return [{'label': 'No appointments available', 'value': None}]





# Callback to manage dynamic dropdowns for treatments
@app.callback(
    [Output('medicalresult-dropdown-container', 'children'),
     Output('medicalresult-dropdown-counter', 'data')],
    [Input('medicalresult_add-dropdown-button', 'n_clicks'),
     Input('medicalresult_remove-dropdown-button', 'n_clicks')],
    [State('medicalresult-dropdown-container', 'children'),
     State('medicalresult-dropdown-counter', 'data')]
)
def update_dropdowns(add_n_clicks, remove_n_clicks, current_children, dropdown_count):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If Add button is clicked
    if button_id == 'medicalresult_add-dropdown-button':
        dropdown_count += 1

        # SQL query to fetch treatment names
        sql = """
            SELECT treatment_id, treatment_m AS treatment_name
            FROM Treatment
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
                        id={'type': 'medicalresult-dynamic-dropdown', 'index': dropdown_count},  # Unique ID for each dropdown
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

    # If Remove button is clicked
    elif button_id == 'medicalresult_remove-dropdown-button' and dropdown_count > 0:
        dropdown_count -= 1
        # Remove the last dropdown from the container
        current_children.pop()

    return current_children, dropdown_count

#Removes Mark as delete during edit mode
@app.callback(
    [
        Output('medicalresult_edit_id', 'data'),
        Output('medicalresult_patient_profile_delete', 'className'),
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def medical_result_load(pathname, urlsearch):
    if pathname == '/medical_records/medical_record_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            medical_edit_id = 0
            patient_profile_delete = 'd-none'
        else:
            medical_edit_id = int(parse_qs(parsed.query).get('id', [0])[0])
            patient_profile_delete = ''
        
        return [medical_edit_id, patient_profile_delete]
    
    else:
        raise PreventUpdate
