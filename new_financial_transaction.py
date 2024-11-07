import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        # Header with Back Button
        dbc.Row(
            [
                dbc.Col(html.H2("Add New Financial Transaction Record", style={'font-size': '25px'}), width="auto"),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        color="secondary",
                        href="/financial_transaction",
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

        dbc.Alert(id='transactionprofile_alert', is_open=False), # For feedback purposes

        # Form Layout
        dbc.Form(
            [
                # Payment Date
                dbc.Row(
                    [
                        dbc.Label("Payment Date", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='date',
                                id='financialtransaction_date',
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8, 
                        ),
                    ],
                    className='mb-3'
                ),

                # Payment Amount
                dbc.Row(
                    [
                        dbc.Label("Payment Amount", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_paymentamount',
                                placeholder='Enter Payment Amount',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Payment Status
                dbc.Row(
                    [
                        dbc.Label("Payment Status", width=2),
                        dbc.Col(
                            dbc.Select(
                                id='financialtrasaction_status',
                                options=[
                                {'label': 'Paid', 'value': 'Paid'},
                                {'label': 'Partially Paid', 'value': 'Partially_Paid'},
                                {'label': 'Not Paid', 'value': 'Not_Paid'}
                                ],
                                placeholder='Payment Status',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8,
                        ),
                    ],
                    className='mb-3'
                ),

                # Paid Amount
                dbc.Row(
                    [
                        dbc.Label("Paid Amount", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_paidamount',
                                placeholder='Enter Paid Amount',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Remarks
                dbc.Row(
                    [
                        dbc.Label("Remarks", width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='financialtransaction_remarks',
                                placeholder='Remarks',
                                className="form-control",
                                style={"borderRadius": "20px", "backgroundColor": "#f0f2f5", "fontSize": "18px"}
                            ),
                            width=8
                        ),
                    ],
                    className="mb-3"
                ),

                # Submit Button
                dbc.Button(
                    "Submit",
                    color="primary", 
                    className="mt-3",
                    n_clicks=0, # Initialize number of clicks
                    style={
                        "borderRadius": "20px",
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "backgroundColor": "#194D62",
                        "color": "white"
                    },
                )
            ]
        )
    ],
    className="container mt-4"
)

        # dbc.Modal( # Modal = dialog box; feedback for successful saving.
        #     [
        #         dbc.ModalHeader(
        #             html.H4('Save Success')
        #         ),
        #         dbc.ModalBody(
        #             'Financial Transaction was successfully recorded!'
        #         ),
        #         dbc.ModalFooter(
        #             dbc.Button(
        #                 "Proceed",
        #                 href='/financial_transaction_management' # Clicking this would lead to a change of pages
        #             )
        #         )
        #     ],
        #     centered=True,
        #     id='new_financialtransaction_successmodal',
        #     backdrop='static' # Dialog box does not go away if you click at the background
        # )

