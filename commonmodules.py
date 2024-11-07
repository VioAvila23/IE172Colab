import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define Navbar styling and active state
navlink_style = {
    'color': '#062937',
    'font-size': '20px',
    'margin': '0 1.5em',  # Adjusted left and right margin for consistent spacing
    'padding': '10px 0',  # Added padding for vertical alignment
}
navlink_active_style = {
    'color': '#062937',
    'font-size': '20px',
    'borderBottom': '3px solid blue',
    'margin': '0 1.5em',
    'padding': '10px 0',
}

# Navbar component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.Img(
                        src="https://img.freepik.com/premium-vector/teeth-tooth-logo-design-vector-illustration_898026-1268.jpg",
                        height="80px",
                        width="90px",
                        style={'margin-right': '20px'}
                    ), width="auto"),  # Set width to auto to keep image and brand close
                    dbc.Col(dbc.NavbarBrand(
                        "Dental Studio",
                        className="ms-2",
                        style={'color': '#062937', 'font-weight': 'bold', 'font-size': '33px'}
                    ), width="auto"),
                ],
                align="center",
                className="g-0 me-auto",
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/home", id="nav-home", style=navlink_style),
                    dbc.NavLink("Appointment", href="/appointment", id="nav-appointment", style=navlink_style),
                    dbc.NavLink("Patient Profile", href="/patient_profile", id="nav-patient-profile", style=navlink_style),
                    dbc.NavLink("Medical Records", href="/medical_records", id="nav-medical-records", style=navlink_style),
                    dbc.NavLink("Financial Transaction", href="/financial_transaction", id="nav-financial-transaction", style=navlink_style),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ],
        fluid=True,  # Full-width container for better spacing control
    ),
    color="#FFF",
    dark=False,
    className="mb-4",
    style={'padding': '15px', 'borderBottom': '2px solid #e3e3e3'}
)