import webbrowser
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Importing your app variable from app.py so we can use it
from app import app
from apps import commonmodules as cm
from apps.patient_profile import patient_management, patient_management_profile
from apps import home

# Define styles for active and inactive navbar links
navlink_style = {'color': '#062937', 'font-size': '20px', 'margin-right': '2.5em'}
navlink_active_style = {'color': '#062937', 'font-size': '20px', 'borderBottom': '2px solid blue', 'margin-right': '2.5em'}

# Main layout of the app
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        cm.navbar,
        html.Div(id='page_content', className='m-2 p-2'),
    ]
)

# Callback to update the active link styling based on URL path
@app.callback(
    [Output("nav-home", "style"),
     Output("nav-appointment", "style"),
     Output("nav-patient-profile", "style"),
     Output("nav-financial-transaction", "style")],
    [Input("url", "pathname")]
)
def update_active_link_style(pathname):
    # Default all styles to non-active
    styles = [navlink_style, navlink_style, navlink_style, navlink_style]
    
    # Set active style based on URL path
    if pathname == "/home":
        styles[0] = navlink_active_style
    elif pathname == "/appointment":
        styles[1] = navlink_active_style
    elif pathname == "/patient_profile":
        styles[2] = navlink_active_style
    elif pathname == "/financial_transaction":
        styles[3] = navlink_active_style
    
    return styles

# Callback to display the correct page content based on URL path
@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def display_page_content(pathname):
    # Display content based on the pathname
    if pathname == '/' or pathname == '/home':
        return home.layout  # Assumes home.layout is defined in the `home` module
    elif pathname == '/appointment':
        return html.Div("Appointment Page Content")  # Placeholder for the Appointment page
    elif pathname == '/patient_profile':
        return patient_management.layout
    elif pathname == '/patient_profile/patient_management_profile':
        return patient_management_profile.layout  # Placeholder for the Patient Profile page
    elif pathname == '/financial_transaction':
        return html.Div("Financial Transaction Page Content")  # Placeholder for Financial Transaction page
    else:
        # Display a 404 error message for unknown paths
        return html.Div("404 - Page not found", style={'color': 'red', 'font-size': '24px', 'text-align': 'center'})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
