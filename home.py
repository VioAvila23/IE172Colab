import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

# Layout definition
layout = dbc.Container(
    [
        dbc.Row(
            [
                # Left column with welcome text
                dbc.Col(
                    [
                        html.H1("WELCOME TO DENTAL CLINIC SYSTEM!", className="display-4 fw-bold text-white"),
                        html.P(
                            "Here, you can easily manage appointments and edit all patient records to keep everything up-to-date and accessible.",
                            className="lead text-white",
                        ),
                    ],
                    md=6,
                    className="align-self-center p-4",  # Add padding inside the left column
                ),
                
                # Right column with main image and smaller images
                dbc.Col(
                    [
                        # Main image with border and padding
                        html.Div(
                            html.Img(src="https://i.pinimg.com/736x/4f/d7/96/4fd7966486f0db87e58a36a081619a62.jpg", className="img-fluid rounded"),  # Replace with main image path
                            style={'border': '2px solid #FFFFFF', 'border-radius': '10px', 'padding': '5px'}
                        ),
                        # Row of smaller images below the main image
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="https://www.drbrettlangston.com/wp-content/uploads/When-Do-You-Need-a-Deep-Teeth-Cleaning-vs.-a-Regular-Cleaning.jpeg", 
                                                 className="img-fluid rounded mt-3", 
                                                 style={'border': '2px solid #FFFFFF', 'border-radius': '10px', 'height': '120px', 'width': '100%'}), width=4),
                                
                                dbc.Col(html.Img(src="https://www.yourdentistryguide.com/wp-content/uploads/2017/11/braces-procedure-min-925x425.jpg", 
                                                 className="img-fluid rounded mt-3", 
                                                 style={'border': '2px solid #FFFFFF', 'border-radius': '10px', 'height': '120px', 'width': '100%'}), width=4),
                                
                                dbc.Col(html.Img(src="https://www.victorianvillagedentalcare.com/wp-content/uploads/2023/01/shutterstock_1294378297.jpg", 
                                                 className="img-fluid rounded mt-3", 
                                                 style={'border': '2px solid #FFFFFF', 'border-radius': '10px', 'height': '120px', 'width': '100%'}), width=4),
                            ],
                            className="mt-3 justify-content-center"
                        ),
                    ],
                    md=6,
                ),
            ],
            className="mb-0",
        ),
    ],
    fluid=True,
    style={'padding': '20px', 'backgroundColor': '#194D62'}  # Updated background color
)
