import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from urllib.parse import parse_qs, urlparse
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate

layout = dbc.Container([
    dcc.Store(id='medicalprofile_id', storage_type='memory', data=0),  # Store to hold patient ID
    

    # Row for patient information display and action buttons
    dbc.Row(
        [
            # Column for patient information display
            dbc.Col(
                [
                    html.Label("Patient Medical Record Information", className="form-label", style={"fontSize": "18px", "fontWeight": "bold"}),

                    # Display Patient Last Name
                    html.Div(
                        [
                            html.Span("Last Name: ", style={"fontWeight": "bold"}),
                            html.Span(id="display_last_name", style={"textDecoration": "underline"})  # Underline styling
                        ],
                        style={"fontSize": "18px", "paddingBottom": "10px"}
                    ),
                    
                    # Display Patient First Name
                    html.Div(
                        [
                            html.Span("First Name: ", style={"fontWeight": "bold"}),
                            html.Span(id="display_first_name", style={"textDecoration": "underline"})  # Underline styling
                        ],
                        style={"fontSize": "18px", "paddingBottom": "10px"}
                    ),
                    
                    # Display Patient Middle Name
                    html.Div(
                        [
                            html.Span("Middle Name: ", style={"fontWeight": "bold"}),
                            html.Span(id="display_middle_name", style={"textDecoration": "underline"})  # Underline styling
                        ],
                        style={"fontSize": "18px", "paddingBottom": "10px"}
                    ),

                    # Display Patient Age
                    html.Div(
                        [
                            html.Span("Age: ", style={"fontWeight": "bold"}),
                            html.Span(id="display_age", style={"textDecoration": "underline"})  # Underline styling
                        ],
                        style={"fontSize": "18px", "paddingBottom": "10px"}
                    ),

                    # Display Patient Sex
                    html.Div(
                        [
                            html.Span("Sex: ", style={"fontWeight": "bold"}),
                            html.Span(id="display_sex", style={"textDecoration": "underline"})  # Underline styling
                        ],
                        style={"fontSize": "18px", "paddingBottom": "10px"}
                    ),
                ],
                md=8,
            ),

            # Column for action buttons aligned to the far right side
            dbc.Col(
                [
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/medical_records",
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "backgroundColor": "#194D62",
                            "color": "white",
                            "width": "200px"  # Set a fixed width for consistency
                        },
                        className="mb-2"  # Margin-bottom for spacing between buttons
                    ),
                    dbc.Button(
                        "Add New Medical Record",
                        color="primary",
                        id="add_record_button",  # Add an ID for the button
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "backgroundColor": "#194D62",
                            "color": "white",
                            "width": "200px"  # Set a fixed width for consistency
                        }
                    ),
                ],
                md="auto",
                className="d-flex flex-column align-items-end ms-auto"  # Align items to the far right
            ),
        ],
        className="mb-4",
        align="center"
    ),

    # Row for the medical records table
    dbc.Row(
        dbc.Col(
            html.Div(
                id="medical-records-table",  # ID for medical records table placeholder
                className="text-center",
                style={"fontSize": "18px", "color": "#666", "padding": "50px", "height": "1000px"}  # Adjust height here
            ),
            width=12,
            style={"border": "2px solid #194D62", "borderRadius": "10px", "padding": "20px"}
        ),
    ),
], fluid=True, style={"padding": "20px", "backgroundColor": "#f8f9fa"})

# Callback to load medical profile ID from the URL
@app.callback(
    [Output('medicalprofile_id', 'data')],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def medical_record_load(pathname, urlsearch):
    if pathname == '/medical_records/medical_record_profile':
        parsed = urlparse(urlsearch)
        medicalprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
        return [medicalprofile_id]
    else:
        raise PreventUpdate

# Callback to update the "Add New Medical Record" button href dynamically
@app.callback(
    Output("add_record_button", "href"),
    [Input("medicalprofile_id", "data")]
)
def update_add_record_button_href(medicalprofile_id):
    if medicalprofile_id:
        return f"/medical_records/medical_record_management_profile?mode=add&id={medicalprofile_id}"
    return "/medical_records/medical_record_management_profile?mode=add"  # Default URL if no ID is set

# Callback to display the medical records table
@app.callback(
    [Output('medical-records-table', 'children')],
    [Input('medicalprofile_id', 'data')]
)
def display_medical_records(medicalprofile_id):
    sql = """SELECT 
        mr.medical_result_id,
        a.appointment_date,
        t.treatment_m,
        mr.medical_condition,
        mr.medical_diagnosis,
        mr.medical_prescription
    FROM 
        Patient p
    INNER JOIN 
        Appointment a ON p.patient_id = a.patient_id
    INNER JOIN 
        Appointment_treatment at ON a.appointment_id = at.appointment_id
    INNER JOIN 
        Treatment t ON at.treatment_id = t.treatment_id
    INNER JOIN 
        Medical_result mr ON a.medical_result_id = mr.medical_result_id
    WHERE 
        p.patient_id = %s
    ORDER BY 
        a.appointment_date DESC;
    """
    val = [medicalprofile_id]

    col = ["Medical Result ID","Date", "Treatment Done", "Condition", "Diagnosis", "Prescription"]

    df = getDataFromDB(sql, val, col)

    if df.empty:
        return [html.Div("No records found.", className="text-center")]

    # Add an "Edit" button that includes the current medicalprofile_id in the URL
    df['Action'] = [
        html.Div(
            dbc.Button("Edit", color='warning', size='sm', 
                       href=f'/medical_records/medical_record_management_profile?mode=edit&id={row["Medical Result ID"]}'
                       ),
            className='text-center'
        ) for idx, row in df.iterrows() 
    ]
    display_columns = ["Medical Result ID","Date", "Treatment Done", "Condition", "Diagnosis", "Prescription", "Action"]

    table = dbc.Table.from_dataframe(
        df[display_columns], 
        striped=True, bordered=True, hover=True, size='sm', style={'textAlign': 'center'}
    )

    return [table]

# Callback to display profile information
@app.callback(
    [
        Output('display_last_name', 'children'),
        Output('display_first_name', 'children'),
        Output('display_middle_name', 'children'),
        Output('display_age', 'children'),
        Output('display_sex', 'children'),
    ],
    [Input('medicalprofile_id', 'data')]
)
def displayprofile(medicalprofile_id):
    if medicalprofile_id == 0:
        raise PreventUpdate

    # SQL query to fetch the patient's profile information
    sql = """
        SELECT 
            patient_last_m, 
            patient_first_m, 
            patient_middle_m,
            age, 
            sex
        FROM 
            Patient
        WHERE 
            patient_id = %s
    """
    val = [medicalprofile_id]

    # Fetch data from the database
    col = ['Last Name', 'First Name', 'Middle Name', 'Age', 'Sex']
    df = getDataFromDB(sql, val, col)

    if df.empty:
        # If no data is found, return placeholders or empty strings
        return ["Not available", "Not available", "Not available", "Not available", "Not available"]

    # Extract values from the DataFrame
    last_name = df.iloc[0]['Last Name']
    first_name = df.iloc[0]['First Name']
    middle_name = df.iloc[0]['Middle Name']
    age = df.iloc[0]['Age']
    sex = df.iloc[0]['Sex']

    # Return the values to populate the placeholders
    return last_name, first_name, middle_name, age, sex
