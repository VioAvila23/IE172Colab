from urllib.parse import parse_qs, urlparse
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dash import Input, Output, State
from app import app
from dbconnect import getDataFromDB, modifyDB
from dash.exceptions import PreventUpdate


layout = html.Div(
    [
        dcc.Store(id='treatmentprofile_id', storage_type='memory', data=0),
        dbc.Row(
            [
                dbc.Col(html.H2(id="treatment_profile_header", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/treatment",
                        style={
                            "borderRadius": "20px",
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "marginRight": "10px",
                            "backgroundColor": "#194D62"
                        }
                    ),
                    width="auto"
                ),
            ],
            align="center",
            className="mb-4"
        ),
        
        html.Hr(),
        
        # Treatment Form Layout
        dbc.Form(
            [
                # Treatment Name
                dbc.Row(
                    [
                        dbc.Label("Treatment Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='treatment_name',
                                placeholder='Enter Treatment Name',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Treatment Description
                dbc.Row(
                    [
                        dbc.Label("Description", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='treatment_description',
                                placeholder='Enter Treatment Description',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                
                # Treatment Price
                dbc.Row(
                    [
                        dbc.Label("Price", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='treatment_price',
                                placeholder='Enter Treatment Price',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),
                html.Div(
                    [
                        dbc.Checklist(
                            id='treatment_profile_deletediv',
                            options=[dict(value=1, label="Mark as Deleted")],
                            value=[]
                        )
                    ],
                    id='treatment_profile_deletediv'
                ),

                dbc.Button(
                    "Submit", 
                    color="primary", 
                    className="mt-3",
                    id='treatmentsubmit_button',
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                ),
                
                dbc.Alert(id='treatment_submit_alert', is_open=False)
            ]
        ),
    ],
    className="container mt-4"
)
@app.callback(
    [
        Output('treatmentprofile_id', 'data'),
        Output('treatment_profile_deletediv', 'className')
    ],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def treatment_profile_load(pathname, urlsearch):
    if pathname == '/treatment/treatment_management_profile':
        parsed = urlparse(urlsearch)
        create_mode = parse_qs(parsed.query).get('mode', [''])[0]

        if create_mode == 'add':
            treatmentprofile_id = 0
            treatment_profile_deletediv = 'd-none'
        else:
            treatmentprofile_id = int(parse_qs(parsed.query).get('id', [0])[0])
            treatment_profile_deletediv = ''
        
        return [treatmentprofile_id, treatment_profile_deletediv]
    else:
        raise PreventUpdate
    
@app.callback(
    Output('treatment_profile_header', 'children'),
    Input('url', 'search')
)
def update_treatment_header(urlsearch):
    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]
    
    if create_mode == 'add':
        return "Add New Treatment"
    else:
        return "Edit Treatment"
    
@app.callback(
    [Output('treatment_submit_alert', 'color'),
     Output('treatment_submit_alert', 'children'),
     Output('treatment_submit_alert', 'is_open')],
    [Input('treatmentsubmit_button', 'n_clicks')],
    [State('treatment_name', 'value'),
     State('treatment_description', 'value'),
     State('treatment_price', 'value'),
     State('url', 'search'),
     State('treatmentprofile_id', 'data'),
     State('treatment_profile_deletediv', 'value')]
)
def submit_treatment_form(n_clicks, treatment_name, treatment_description, treatment_price, urlsearch, treatmentprofile_id,delete):
    
    ctx = dash.callback_context
    if not ctx.triggered or not n_clicks:
        raise PreventUpdate

    parsed = urlparse(urlsearch)
    create_mode = parse_qs(parsed.query).get('mode', [''])[0]

    # Check for missing values in the required fields
    if not all([treatment_name, treatment_description, treatment_price]):
        return 'danger', 'Please fill in all required fields.', True

    # SQL to insert or update the database
    if create_mode == 'add':
        sql = """INSERT INTO Treatment (treatment_m, treatment_description, treatment_price)
                 VALUES (%s, %s, %s);"""
        
        values = [treatment_name, treatment_description, treatment_price]
    
    elif create_mode == 'edit':
        if delete:
            # Mark as deleted
            sql = """UPDATE Treatment
                     SET treatment_delete = true
                     WHERE treatment_id = %s;"""
            values = [treatmentprofile_id]
        else:

            sql = """UPDATE Treatment
                    SET treatment_m = %s,
                        treatment_description = %s,
                        treatment_price = %s
                    WHERE treatment_id = %s;"""
            
            values = [treatment_name, treatment_description, treatment_price, treatmentprofile_id]
    else:
        raise PreventUpdate

    try:
        modifyDB(sql, values)
        return 'success', 'Treatment Submitted successfully!', True
    except Exception as et:
        return 'danger', f'Error Occurred: {et}', True



@app.callback(
    [Output('treatment_name', 'value'),
     Output('treatment_description', 'value'),
     Output('treatment_price', 'value')],
    [Input('treatmentprofile_id', 'modified_timestamp')],
    [State('treatmentprofile_id', 'data')]
)
def treatment_profile_populate(timestamp, treatmentprofile_id):
    if treatmentprofile_id > 0:
        sql = """SELECT treatment_m, treatment_description, treatment_price
                 FROM Treatment
                 WHERE treatment_id = %s"""
        values = [treatmentprofile_id]
        col = ['treatment_name', 'treatment_description', 'treatment_price']

        df = getDataFromDB(sql, values, col)

        treatment_name = df['treatment_name'][0]
        treatment_description = df['treatment_description'][0]
        treatment_price = df['treatment_price'][0]

        return [treatment_name, treatment_description, treatment_price]
    else:
        raise PreventUpdate
