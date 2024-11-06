import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define Navbar styling and active state
navlink_style = {'color': '#062937', 'font-size': '20px', 'margin-right': '2.5em'}  # Increase margin-right for spacing
navlink_active_style = {'color': '#062937', 'font-size': '20px', 'borderBottom': '3px solid blue', 'margin-right': '2.5em'}

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
                    )),
                    dbc.Col(dbc.NavbarBrand(
                        "Dental Studio",
                        className="ms-2",
                        style={'color': '#062937', 'font-weight': 'bold', 'font-size': '33px', 'margin-right': '0.5em'}
                    )),
                ],
                align="center",
                className="g-0 me-auto",
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/home", id="nav-home", className="px-3", style=navlink_style),
                    dbc.NavLink("Appointment", href="/appointment", id="nav-appointment", className="px-3", style=navlink_style),
                    dbc.NavLink("Patient Profile", href="/patient_profile", id="nav-patient-profile", className="px-3", style=navlink_style),
                    dbc.NavLink("Financial Transaction", href="/financial_transaction", id="nav-financial-transaction", className="px-3", style=navlink_style),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ]
    ),
    color="#FFF",
    dark=False,
    className="mb-4",
    style={'padding': '15px', 'borderBottom': '2px solid #e3e3e3', 'margin-bottom':'0'}
)