import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs, urlparse
from dbconnect import getDataFromDB

layout = dbc.Container(
    [
        # Header Section
        html.Div(
            [
                html.H3("Dental Studio", className="text-center", style={"fontWeight": "bold"}),
                html.P(
                    "5, C Himes Square, 77 Congressional Ave Ext, Quezon City, 1107 Metro Manila",
                    className="text-center",
                ),
                html.H4("Receipt", className="text-center mt-3", style={"fontWeight": "bold"}),
            ],
            className="mb-4",
        ),
        
        # Top Information Section
        html.Div(
            [
                # First Row: Transaction ID and Payment Status
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label("Transaction ID:", style={"fontWeight": "bold"}),
                                        width=4,
                                        className="text-right align-self-center",
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="generate_transac_transactionid_id",
                                            type="text",
                                            className="form-control",
                                            disabled=True,
                                        ),
                                        width=8,
                                    ),
                                ],
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label("Payment Status:", style={"fontWeight": "bold"}),
                                        width=4,
                                        className="text-right align-self-center",
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="generate_transac_paymentstatus_id",
                                            type="text",
                                            className="form-control",
                                            disabled=True,
                                        ),
                                        width=8,
                                    ),
                                ],
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                # Second Row: Payment Date
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label("Payment Date:", style={"fontWeight": "bold"}),
                                        width=4,
                                        className="text-right align-self-center",
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="generate_transac_paymentdate_id",
                                            type="text",
                                            className="form-control",
                                            disabled=True,
                                        ),
                                        width=8,
                                    ),
                                ],
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),

                # Third Row: Patient Name
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label("Patient Name:", style={"fontWeight": "bold"}),
                                        width=4,
                                        className="text-right align-self-center",
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="generate_transac_patientname_id",
                                            type="text",
                                            className="form-control",
                                            disabled=True,
                                        ),
                                        width=8,
                                    ),
                                ],
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
            ],
            className="p-3 bg-light rounded shadow-sm",
        ),
        
        # Table Section
        html.Div(
            id="generate_transac_tableholder_id",
            style={
                "border": "1px solid black",
                "borderRadius": "5px",
                "padding": "20px",
                "minHeight": "300px",
                "marginBottom": "20px",
            },
            className="text-center",
        ),

        # Bottom Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Remarks:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                        dbc.Input(
                            id="generate_transac_remarks_id",
                            type="text",
                            className="form-control",
                            disabled=True,
                            style={"width": "100%"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Label("Total:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                                dbc.Input(
                                    id="generate_transac_totalamount_id",
                                    type="text",
                                    className="form-control",
                                    disabled=True,
                                    style={"width": "100%"},
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                html.Label("Amount Paid:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                                dbc.Input(
                                    id="generate_transac_amountpaid_id",
                                    type="text",
                                    className="form-control",
                                    disabled=True,
                                    style={"width": "100%"},
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                html.Label("Remaining:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                                dbc.Input(
                                    id="generate_transac_remainingamount_id",
                                    type="text",
                                    className="form-control",
                                    disabled=True,
                                    style={"width": "100%"},
                                ),
                            ],
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mt-4",
        ),
    ],
    fluid=True,
    style={"padding": "20px"},
)

@app.callback(
    [
        Output("generate_transac_transactionid_id", "value"),
        Output("generate_transac_paymentstatus_id", "value"),
        Output("generate_transac_paymentstatus_id", "style"),
        Output("generate_transac_paymentdate_id", "value"),
        Output("generate_transac_patientname_id", "value"),
    ],
    Input("url", "search"),
)
def populate_top_section(urlsearch):
    if not urlsearch:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    payment_id = int(parse_qs(parsed.query).get("id", [0])[0])
    
    sql = """
        SELECT 
            p.payment_id, 
            p.payment_status, 
            TO_CHAR(p.payment_date, 'DD, Month YYYY') AS formatted_date, 
            CONCAT(pt.patient_first_m, ' ', pt.patient_last_m) AS patient_name
        FROM Payment p
        JOIN Appointment a ON p.payment_id = a.payment_id
        JOIN Patient pt ON a.patient_id = pt.patient_id
        WHERE p.payment_id = %s AND p.payment_delete = false
    """
    val = [payment_id]
    col = ["Transaction ID", "Payment Status", "Payment Date", "Patient Name"]
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return ["N/A", "", {}, "", ""]

    row = df.iloc[0]
    
    # Dynamic style based on payment status
    payment_status = row["Payment Status"]
    if payment_status == "Paid":
        style = {"backgroundColor": "green", "color": "white"}
    elif payment_status == "Partially Paid":
        style = {"backgroundColor": "yellow", "color": "black"}
    else:  # Not Paid
        style = {"backgroundColor": "red", "color": "white"}
    
    return (
        row["Transaction ID"],
        payment_status,
        style,
        row["Payment Date"],
        row["Patient Name"],
    )


@app.callback(
    Output("generate_transac_tableholder_id", "children"),
    Input("url", "search"),
)
def populate_table_section(urlsearch):
    if not urlsearch:
        raise PreventUpdate

    # Parse the URL to get the payment ID
    parsed = urlparse(urlsearch)
    payment_id = int(parse_qs(parsed.query).get("id", [0])[0])
    
    # SQL query to fetch the required fields
    sql = """
        SELECT 
    t.treatment_m AS "Treatment Name", 
    at.quantity AS Quantity, 
    t.treatment_price AS "Price per Item", 
    (t.treatment_price * at.quantity) AS Total
FROM Appointment_treatment at
JOIN Treatment t ON at.treatment_id = t.treatment_id
JOIN Appointment a ON at.appointment_id = a.appointment_id
WHERE a.payment_id = %s 
  AND at.appointment_treatment_delete = false
  AND (t.treatment_delete = false OR (t.treatment_delete = true AND t.treatment_id != 6))

    """
    val = [payment_id]
    col = ["Treatment Name", "Quantity", "Price per Item", "Total"]
    
    # Fetch data from the database
    df = getDataFromDB(sql, val, col)
    
    # Check if the query returned results
    if df.empty:
        return html.Div("No treatments found", className="text-center")

    # Generate a styled Dash Table
    return dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        size="sm",
        style={"textAlign": "center"},
    )

@app.callback(
    [
        Output("generate_transac_remarks_id", "value"),
        Output("generate_transac_totalamount_id", "value"),
        Output("generate_transac_amountpaid_id", "value"),
        Output("generate_transac_remainingamount_id", "value"),
    ],
    Input("url", "search"),
)
def populate_bottom_section(urlsearch):
    if not urlsearch:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    payment_id = int(parse_qs(parsed.query).get("id", [0])[0])
    
    sql = """
        SELECT 
            p.remarks, 
            SUM(t.treatment_price * at.quantity) AS total_amount,
            p.paid_amount, 
            (SUM(t.treatment_price * at.quantity) - p.paid_amount) AS remaining_amount
        FROM Payment p
        JOIN Appointment a ON p.payment_id = a.payment_id
        JOIN Appointment_treatment at ON a.appointment_id = at.appointment_id
        JOIN Treatment t ON at.treatment_id = t.treatment_id
        WHERE p.payment_id = %s AND p.payment_delete = false AND at.appointment_treatment_delete = false
        GROUP BY p.payment_id, p.remarks, p.paid_amount
    """
    val = [payment_id]
    col = ["Remarks", "Total", "Paid", "Remaining"]
    df = getDataFromDB(sql, val, col)
    
    if df.empty:
        return ["", "PHP 0.00", "PHP 0.00", "PHP 0.00"]

    row = df.iloc[0]

    # Format the currency values to PHP format with .00
    total = f"PHP {row['Total']:.2f}"
    paid = f"PHP {row['Paid']:.2f}"
    remaining = f"PHP {row['Remaining']:.2f}"

    return row["Remarks"], total, paid, remaining
