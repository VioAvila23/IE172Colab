from dash import html, dcc

layout = html.Div(
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'backgroundColor': '#ffffff',
        'flexDirection': 'row',  # Updated from column to row to align items side by side
    },
    children=[
        # Left Section: Dental Studio Database Text
        html.Div(
            children=[
                html.Img(src="https://img.freepik.com/premium-vector/teeth-tooth-logo-design-vector-illustration_898026-1268.jpg", style={'width': '150px', 'marginBottom': '20px'}),  # Adjusted logo size
                html.H1("Dental Studio Database", style={
                    'fontSize': '40px',
                    'fontWeight': 'bold',
                    'color': '#194D62',
                    'textAlign': 'center',
                    'marginTop': '0',
                    'marginBottom': '20px'
                }),
                html.P("Welcome to the admin portal. Please log in to continue.",
                       style={
                           'fontSize': '18px',
                           'color': '#555',
                           'textAlign': 'center'
                       })
            ],
            style={
                'width': '50%',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }
        ),
        
        # Right Section: Log In Section
        html.Div(
            style={
                'backgroundColor': '#fff',
                'borderRadius': '20px',
                'padding': '50px',
                'boxShadow': '0px 6px 6px rgba(0, 0, 0, 0.25)',
                'width': '450px',
                'height': '470px',
                'textAlign': 'center',
            },
            children=[
                html.H2("LOG IN", style={'fontSize': '28px', 'textAlign': 'left', 'marginBottom': '30px', 'fontWeight': 'bold', 'color': '#2E2C2C'}),
                html.Label("Username", style={'display': 'block', 'textAlign': 'left', 'fontSize': '14px', 'color': '#2E2C2C'}),
                dcc.Input(id='username', type='text', placeholder="Username",
                          style={'width': '100%', 'padding': '12px', 'marginBottom': '20px', 'border': '1px solid #B7B7B7', 'borderRadius': '10px'}),
                html.Label("Password", style={'display': 'block', 'textAlign': 'left', 'fontSize': '14px', 'color': '#2E2C2C'}),
                dcc.Input(id='password', type='password', placeholder="Password",
                          style={'width': '100%', 'padding': '12px', 'marginBottom': '30px', 'border': '1px solid #B7B7B7', 'borderRadius': '10px'}),
                html.Button("LOG IN", id='login-button', n_clicks=0,
                            style={
                                'backgroundColor': '#194D62', 
                                'color': '#fff', 
                                'width': '100%', 
                                'height': '55px',
                                'borderRadius': '10px',
                                'fontWeight': '600',
                                'border': '0px solid #B7B7B7',
                                'boxShadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                                'fontSize': '16px',
                            }),
                html.Div(id='login-error', style={'color': 'red', 'marginTop': '10px'}),

                html.Div(
                    children=[
                        html.P("Don't have an account yet?", style={
                            'fontSize': '14px',
                            'color': '#2E2C2C',
                            'marginTop': '20px',
                            'marginBottom': '5px'
                        }),
                        dcc.Link("Sign up here", href='/signup', refresh=True, style={
                            'color': '#194D62',
                            'fontWeight': '600',
                            'fontSize': '14px',
                            'textDecoration': 'none'
                        })
                    ]
                ),
            ]
        )
    ]
)