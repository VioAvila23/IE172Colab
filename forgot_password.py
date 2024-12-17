import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'backgroundColor': '#f8f9fa',  # Light background for better contrast
    },
    children=[
        html.Div(
            style={
                'backgroundColor': '#ffffff',
                'borderRadius': '10px',
                'padding': '40px',
                'boxShadow': '0px 6px 12px rgba(0, 0, 0, 0.15)',
                'width': '400px',
                'textAlign': 'center',
            },
            children=[
                # Header
                html.H2("Reset Password", style={
                    'marginBottom': '20px',
                    'fontWeight': 'bold',
                    'color': '#194D62',
                }),
                html.P(
                    "Enter your username to reset your password.",
                    style={'marginBottom': '30px', 'color': '#555'}
                ),
                
                # Alert for errors
                dbc.Alert(
                    "Please provide a valid username and matching passwords.",
                    color="danger",
                    id='forgot_password_alert',
                    is_open=False,
                    dismissable=True,
                ),
                
                # Username input
                dbc.Row(
                    [
                        dbc.Label("Username", html_for="reset_username", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="reset_username",
                                placeholder="Enter your username",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                
                # New Password input
                dbc.Row(
                    [
                        dbc.Label("New Password", html_for="reset_password", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="reset_password",
                                placeholder="Enter a new password",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                
                # Confirm Password input
                dbc.Row(
                    [
                        dbc.Label("Confirm Password", html_for="reset_passwordconf", width=12, style={
                            'textAlign': 'left', 'fontWeight': 'bold', 'marginBottom': '5px'
                        }),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="reset_passwordconf",
                                placeholder="Re-type the new password",
                                style={'borderRadius': '5px'}
                            ),
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),
                
                # Reset Button
                dbc.Button(
                    "Reset Password",
                    id="reset_passwordbtn",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'fontWeight': 'bold',
                        'backgroundColor': '#194D62',
                        'border': 'none',
                        'color': 'white',
                    },
                ),
                
                # Confirmation Modal
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            dbc.ModalTitle("Password Reset Successful"),
                            style={'color': '#194D62'}
                        ),
                        dbc.ModalBody(
                            "Your password has been reset successfully.",
                            id='reset_confirmation',
                            style={'color': '#555'}
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Go to Login",
                                href='/login',
                                color="primary",
                                style={'fontWeight': 'bold'}
                            ),
                        ),
                    ],
                    id="reset_modal",
                    is_open=False,
                ),   
            ]
        ),
    ]
)

# Disable the reset button if passwords do not match
@app.callback(
    Output('reset_passwordbtn', 'disabled'),
    [
        Input('reset_password', 'value'),
        Input('reset_passwordconf', 'value'),
    ]
)
def deactivate_resetbtn(password, passwordconf):
    enablebtn = password and passwordconf and password == passwordconf
    return not enablebtn

# Reset password
@app.callback(
    [
        Output('forgot_password_alert', 'is_open'),
        Output('reset_modal', 'is_open')
    ],
    [
        Input('reset_passwordbtn', 'n_clicks')
    ],
    [
        State('reset_username', 'value'),
        State('reset_password', 'value'),
    ]
)
def reset_password(n_clicks, username, new_password):
    openalert = openmodal = False
    if n_clicks:
        if username and new_password:
            # Check if the username exists in the database
            check_sql = """SELECT user_name FROM users WHERE user_name = %s"""
            result = db.getDataFromDB(check_sql, [username], ['user_name'])


            if not result.empty:  # If the user exists
                # Update the user's password
                update_sql = """UPDATE users SET user_password = %s WHERE user_name = %s"""
                
                # Encrypt the new password
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()
                new_password_hashed = encrypt_string(new_password)
                
                db.modifyDB(update_sql, [new_password_hashed, username])
                openmodal = True
            else:
                openalert = True  # Show error if username does not exist
        else:
            openalert = True  # Show error if fields are incomplete
    else:
        raise PreventUpdate

    return [openalert, openmodal]

