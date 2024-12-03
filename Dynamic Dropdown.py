import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import MATCH, ALL

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Options available for the dropdown
choices = ["Chocolate", "Brownies"]

# App layout
app.layout = html.Div([
    html.H1("Dynamic Dropdown Example"),
    
    # Dropdown to select Chocolate or Brownies (no category selection)
    dcc.Dropdown(
        id='dropdown-1',
        options=[{'label': choice, 'value': choice} for choice in choices],
        placeholder="Select Chocolate or Brownies",
    ),
    
    # Dynamic dropdowns will be added here
    html.Div(id='dropdown-container', children=[]),

    # Button to add another dropdown
    dbc.Button("Add Dropdown", id="add-dropdown-button", n_clicks=0, color="primary"),

    # Output text displaying selected items from each dropdown
    html.Div(id='output-text', children="Output for dropdown 1: , dropdown 2: ")
])

# Callback to update item dropdown based on selected category
@app.callback(
    [Output('dropdown-container', 'children'),
     Output('output-text', 'children')],
    [Input('add-dropdown-button', 'n_clicks'),
     Input('dropdown-1', 'value')],
    [State('dropdown-container', 'children'),
     State({'type': 'dynamic-dropdown', 'index': ALL}, 'value')]  # Get values of all dynamic dropdowns
)
def add_dropdown(n_clicks, selected_value, current_children, dropdown_values):
    # Initialize the text output
    output_text = "Output for dropdown "

    # When the button is clicked, add a new dropdown
    if n_clicks > 0:
        new_dropdown = dcc.Dropdown(
            id={'type': 'dynamic-dropdown', 'index': n_clicks},  # Unique ID for each dropdown
            options=[{'label': choice, 'value': choice} for choice in choices],
            placeholder="Select Chocolate or Brownies"
        )
        current_children.append(new_dropdown)

    # Generate output text based on selected values from all dropdowns
    dropdown_index = 1  # Start numbering from 1
    for value in dropdown_values:
        output_text += f"{dropdown_index}: {value if value else 'not selected'}, "
        dropdown_index += 1

    # Add the first dropdown value
    output_text += f"dropdown 1: {selected_value if selected_value else 'not selected'}, "

    # Ensure to strip the last comma and space
    return current_children, output_text.rstrip(', ')

if __name__ == '__main__':
    app.run_server(debug=True)
