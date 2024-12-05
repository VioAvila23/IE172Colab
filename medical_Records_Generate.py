import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs, urlparse
from dbconnect import getDataFromDB



layout = dbc.Container(
    [
        # Header
        html.H3("Medical Record Summary", className="text-center mb-4", style={"fontWeight": "bold"}),

        # Patient Information Section
        html.Div(
            [
                html.H5("Patient Information", className="mb-3", style={"fontWeight": "bold"}),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Patient Identifier:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_patient_id",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Date of Birth:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_dob",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("First Name:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_first_name",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Gender:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_gender",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Middle Name:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_middle_name",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Contact Number:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_contact_number",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Last Name:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_last_name",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Email Address:", className="mb-0", style={"fontWeight": "bold", "textAlign": "right", "marginRight": "5px"}),
                            ],
                            width=2,
                            className="align-self-center text-right",
                        ),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="medical_record_generate_email_address",
                                className="form-control",
                                disabled=True,
                                style={"marginLeft": "-15px"},
                            ),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                ),
            ],
            className="p-3 border rounded bg-light shadow-sm",
        ),

        # Medical Records Summary Information Section
        html.Div(
            [
                html.H5("Medical Records Summary Information", className="mb-3", style={"fontWeight": "bold"}),
                html.Hr(),
                html.Div(
                    id="medical_record_generate_table_holder",
                    className="text-center",
                    style={
                        "minHeight": "400px",
                        "border": "1px solid #ddd",
                        "borderRadius": "5px",
                        "padding": "20px",
                        "backgroundColor": "#f8f9fa",
                        "overflowX": "auto",
                    },
                ),
            ],
            className="p-3 border rounded bg-light shadow-sm mt-4",
        ),
        # Back Button
        html.Div(
            dbc.Button(
                "Back to Medical Records",
                href="/medical_records",
                color="primary",
                className="mt-3",
                style={"width": "200px"},
            ),
            className="text-center",
        ),
    ],
    fluid=True,
    style={"padding": "20px"},
)
# Callback to populate patient information fields
@app.callback(
    [
        Output("medical_record_generate_patient_id", "value"),
        Output("medical_record_generate_dob", "value"),
        Output("medical_record_generate_first_name", "value"),
        Output("medical_record_generate_middle_name", "value"),
        Output("medical_record_generate_last_name", "value"),
        Output("medical_record_generate_gender", "value"),
        Output("medical_record_generate_contact_number", "value"),
        Output("medical_record_generate_email_address", "value"),
    ],
    Input("url", "search"),
)
def populate_patient_information(urlsearch):
    if not urlsearch:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    patient_id = int(parse_qs(parsed.query).get("id", [0])[0])
    
    sql = """
        SELECT patient_id, patient_bd, patient_first_m, patient_middle_m, 
               patient_last_m, sex, patient_cn, patient_email
        FROM Patient
        WHERE patient_id = %s
    """
    val = [patient_id]
    col = ["ID", "DOB", "First Name", "Middle Name", "Last Name", "Gender", "Contact Number", "Email"]
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return [""] * 8

    row = df.iloc[0]
    return row["ID"], row["DOB"], row["First Name"], row["Middle Name"], row["Last Name"], row["Gender"], row["Contact Number"], row["Email"]

# Callback to populate medical records summary table
# Callback to populate medical records summary table
@app.callback(
    Output("medical_record_generate_table_holder", "children"),
    Input("url", "search"),
)
def populate_medical_summary(urlsearch):
    if not urlsearch:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    patient_id = int(parse_qs(parsed.query).get("id", [0])[0])
    
    # Updated SQL query with filters for deletion and ordering by latest records
    sql = """
        SELECT 
            a.appointment_id,
            mr.medical_result_id, 
            TO_CHAR(a.appointment_date, 'DD, Month YYYY') AS formatted_date,
            STRING_AGG(t.treatment_m, ', ') AS treatment, 
            mr.medical_condition,
            mr.medical_diagnosis, 
            mr.medical_prescription
        FROM 
            Appointment a
        JOIN 
            Appointment_treatment at ON a.appointment_id = at.appointment_id
        JOIN 
            Treatment t ON at.treatment_id = t.treatment_id
        JOIN 
            Medical_result mr ON a.medical_result_id = mr.medical_result_id
        WHERE 
            a.patient_id = %s 
            AND a.appointment_delete = false
            AND t.treatment_delete = false
        GROUP BY 
            a.appointment_id, mr.medical_result_id, a.appointment_date, mr.medical_condition,
            mr.medical_diagnosis, mr.medical_prescription
        ORDER BY 
            a.appointment_date DESC
    """
    val = [patient_id]
    col = ["Appointment ID", "Medical Result ID", "Date", "Treatment", "Condition", "Diagnosis", "Prescription"]
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return html.Div("No records found", className="text-center")

    # Convert DataFrame to a Dash Table component with updated column names
    return dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size="sm",
        style={"textAlign": "center"},
    )

