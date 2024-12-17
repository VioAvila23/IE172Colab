import webbrowser
import dash
import dash_bootstrap_components as dbc
import hashlib
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Importing your app variable from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps.patient_profile import patient_management, patient_management_profile
from apps.medical_records import medical_records_management, medical_records_management_profile, medical_records_profile,medical_Records_Generate
from apps.financial_transactions import financial_transaction, new_financial_transaction,financial_generate
from apps.appointment import appointment_management, appointment_management_profile
from apps.treatments import treatment_management, treatment_management_profile
from apps import performance
import dbconnect as db
from apps import log
from apps import signup
from apps import home

# Define styles for active and inactive navbar links
navlink_style = {'color': '#062937', 'font-size': '20px', 'margin-right': '2.5em'}
navlink_active_style = {'color': '#062937', 'font-size': '20px', 'borderBottom': '2px solid blue', 'margin-right': '2.5em'}

# Main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        html.Div(id='navbar-container'),  # Navbar container to toggle visibility
        html.Div(id='page_content', className='m-2 p-2'),
    ]
)

# Callback to update the active link styling based on URL path
@app.callback(
    [Output("nav-home", "style"),
     Output("nav-appointment", "style"),
     Output("nav-patient-profile", "style"),
     Output("nav-medical-records", "style"),
     Output("nav-financial-transaction", "style"),
     Output("nav-treatment", "style"),
     Output("nav-Clinic-Insights","style")
     ],
    [Input("url", "pathname")]
)
def update_active_link_style(pathname):
    styles = [navlink_style] * 7  # Default styles

    if pathname == "/home":
        styles[0] = navlink_active_style
    elif pathname == "/appointment":
        styles[1] = navlink_active_style
    elif pathname == "/patient_profile":
        styles[2] = navlink_active_style
    elif pathname == "/medical_records":
        styles[3] = navlink_active_style
    elif pathname == "/financial_transaction":
        styles[4] = navlink_active_style
    elif pathname == "/treatment":
        styles[5] = navlink_active_style
    elif pathname == "/performance":
        styles[6] = navlink_active_style

    return styles

# Callback to toggle the navbar and render correct page content
@app.callback(
    [Output('navbar-container', 'children'),
     Output('page_content', 'children')],
    Input('url', 'pathname'),
    
)
def display_page_content(pathname):
    # Hide navbar for login page
    if pathname == '/login' or pathname == '/':
        return None, log.layout
    elif pathname == '/signup':
        return None, signup.layout
    elif pathname == '/forgot_password':
        return None, forgot_password.layout
    elif pathname == '/home':
        return cm.navbar, home.layout
    elif pathname == '/appointment':
        return cm.navbar, appointment_management.layout
    elif pathname == '/appointments/appointment_management_profile':
        return cm.navbar, appointment_management_profile.layout
    elif pathname == '/patient_profile':
        return cm.navbar, patient_management.layout
    elif pathname == '/patient_profile/patient_management_profile':
        return cm.navbar, patient_management_profile.layout
    elif pathname == '/medical_records':
        return cm.navbar, medical_records_management.layout
    elif pathname == '/medical_records/medical_record_profile':
        return cm.navbar, medical_records_profile.layout
    elif pathname == '/medical_records/medical_record_management_profile':
        return cm.navbar, medical_records_management_profile.layout
    elif pathname == '/financial_transaction':
        return cm.navbar, financial_transaction.layout
    elif pathname == '/financial_transaction_management/new_transaction':
        return cm.navbar, new_financial_transaction.layout
    elif pathname == '/treatment':
        return cm.navbar, treatment_management.layout
    elif pathname == '/medical_records/medical_record_generate':
        return cm.navbar, medical_Records_Generate.layout
    elif pathname == '/financial_transaction/financial_generate':
        return cm.navbar, financial_generate.layout
    elif pathname == '/performance':
        return cm.navbar, performance.layout
    elif pathname == '/treatment/treatment_management_profile':
        return cm.navbar, treatment_management_profile.layout
    else:
        return cm.navbar, html.Div("404 - Page not found", style={'color': 'red', 'font-size': '24px', 'text-align': 'center'})

@app.callback(
    [Output('url', 'pathname'), Output('login-error', 'children')],
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def handle_login(n_clicks, username, password):
    if n_clicks > 0:  # Ensure the button was clicked
        if not username or not password:
            return dash.no_update, "Please enter both username and password."
        
        def encrypt_string(string):
            return hashlib.sha256(string.encode('utf-8')).hexdigest()
        
        sql = """SELECT user_password FROM users WHERE user_name = %s AND user_delete_ind = false"""
        values = [username]
        df_result = db.getDataFromDB(sql, values, ['user_password'])

        if not df_result.empty:  # Check if user was found
            stored_password = df_result.iloc[0]['user_password']  # Get the first row's password
            if encrypt_string(password) == stored_password:  # Compare the hashed passwords
                return "/home", ""  # Redirect to home
            else:
                return dash.no_update, "Invalid username or password. Please try again."
        else:
            return dash.no_update, "Invalid username or password. Please try again."
    
    raise PreventUpdate  # No action if not clicked

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/login', new=0, autoraise=True)
    app.run_server(debug=False)
