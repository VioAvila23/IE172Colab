import dash
from app import app

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

DENTAL_LOGO = "https://scontent.fmnl17-3.fna.fbcdn.net/v/t39.30808-6/292232767_428188882655248_2314692471339274940_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeH09yCNRLtKwa-455I-79OCj1BixKHk1u2PUGLEoeTW7Y6EZ9LU35cWfpCN2ZSeJtpKDbFl_JUaJhmJ1Xju2_x9&_nc_ohc=u5XYRtL4FQYQ7kNvgEMszGj&_nc_zt=23&_nc_ht=scontent.fmnl17-3.fna&_nc_gid=ANmjMrA7KE0pkXcVBP9In2T&oh=00_AYDmoeNOguPsZ_iK8-JS5e1f1fweNKnupcw_4X-wo9UDKA&oe=672524AA"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=DENTAL_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Dental Studio", className="ms-2",style={"font-size": "1.5rem", "font-weight": "bold"})),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/home",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home",href="/home", active="exact",)),
                        dbc.NavItem(dbc.NavLink("Appointment", href="/appointment",active="exact")),
                        dbc.NavItem(dbc.NavLink("Settle Financial Transactions", href="/settlefinancialtransactions",active="exact")),
                        dbc.NavItem(dbc.NavLink("Patient Records", href="/patientrecords",active="exact"))
                        
                    ],
                    pills=True,
                    className="justify-content-around w-100",  
                    navbar=True,
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=False,
    className ="shadow-sm"
)
