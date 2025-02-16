# layout.py
from dash import html, dcc

def serve_layout():
    return html.Div([
        # Intro (story) section – first page of the scroll.
        html.Div(
            id='intro-page',
            children=[
                html.H1("eat, track, repeat", 
                        style={
                            'textAlign': 'left',
                            'fontFamily': '"Benton Sans Low-DPI", Arial, Helvetica, sans-serif',
                            'fontStyle': 'italic',
                            'fontSize': '48px',
                            'color': '#5A4D41',
                            'marginBottom': '10px'
                        }),
                html.H2("a delicious data story", 
                        style={
                            'textAlign': 'left',
                            'fontFamily': '"Benton Sans Low-DPI", Arial, Helvetica, sans-serif',
                            'fontStyle': 'italic',
                            'fontSize': '24px',
                            'color': '#5A4D41',
                            'marginBottom': '20px'
                        }),
                html.Div(
                    id='intro-text',
                    children=[
                        html.Div(
                            children=html.P("I'm tracking my food intake and related symptoms for health reasons.",
                                            style={
                                                'textAlign': 'left',
                                                'fontFamily': '"Tableau Book", Tableau, Arial, sans-serif',
                                                'color': 'darkgrey',
                                                'fontSize': '14px',
                                                'margin': '0',
                                                'padding': '10px'
                                            }),
                            style={'width': '300px', 'marginBottom': '10px'}
                        ),
                        html.Div(
                            children=html.P("This dashboard presents my personal data and insights in a clear, data‐driven way.",
                                            style={
                                                'textAlign': 'left',
                                                'fontFamily': '"Tableau Book", Tableau, Arial, sans-serif',
                                                'color': 'darkgrey',
                                                'fontSize': '14px',
                                                'margin': '0',
                                                'padding': '10px'
                                            }),
                            style={'width': '300px'}
                        )
                    ],
                    style={'textAlign': 'left', 'marginBottom': '20px'}
                ),
                html.P(
                    [
                        "I got inspired by this ",
                        html.A("Iron Viz", 
                               href="https://public.tableau.com/app/profile/jusdespommes/viz/IronViz-Coruna/Coruna",
                               style={
                                   'color': 'darkgrey',
                                   'textDecoration': 'underline'
                               }),
                        " from alex."
                    ],
                    style={
                        'textAlign': 'left',
                        'fontFamily': '"Tableau Book", Tableau, Arial, sans-serif',
                        'color': 'darkgrey',
                        'fontSize': '12px',
                        'marginTop': '20px',
                        'fontStyle': 'italic'
                    }
                )
            ],
            style={
                'padding': '50px',
                'maxWidth': '1000px',
                'margin': '0 auto',
                'backgroundColor': '#F6F6F7',
                'minHeight': '80vh',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
            }
        ),
        # Dashboard content section – appears below the intro.
        html.Div(
            id='dashboard-content',
            children=[
                # Section 01: Meal Distribution (replacing Meal Frequency)
                html.Div([
                    html.Span("01", style={'fontSize': '32px', 'color': '#D3D3D3', 'fontWeight': 'bold'}),
                    html.Span(" meal distribution", style={'fontSize': '32px', 'fontStyle': 'italic', 'color': '#5A4D41'})
                ], style={'marginBottom': '20px'}),
                dcc.Graph(id='meal-distribution-chart', style={'height': '500px'}),
                
                # Section 02: Most Common Cooking Methods
                html.Div([
                    html.Span("02", style={'fontSize': '32px', 'color': '#D3D3D3', 'fontWeight': 'bold'}),
                    html.Span(" most common cooking methods", style={'fontSize': '32px', 'fontStyle': 'italic', 'color': '#5A4D41'})
                ], style={'marginTop': '50px', 'marginBottom': '20px'}),
                html.Div(
                    dcc.Slider(min=1, max=10, step=1, value=5, id='cooking-method-slider'),
                    style={'marginBottom': '20px'}
                ),
                dcc.Graph(id='cooking-method-chart', style={'height': '400px'}),
                
                # Section 03: Average Meal Times by Weekday
                html.Div([
                    html.Span("03", style={'fontSize': '32px', 'color': '#D3D3D3', 'fontWeight': 'bold'}),
                    html.Span(" average meal times by weekday", style={'fontSize': '32px', 'fontStyle': 'italic', 'color': '#5A4D41'})
                ], style={'marginTop': '50px', 'marginBottom': '20px'}),
                dcc.Graph(id='average-meal-time-chart', style={'height': '400px'})
            ],
            style={
                'padding': '50px',
                'maxWidth': '1000px',
                'margin': '0 auto',
                'backgroundColor': '#F6F6F7'
            }
        )
    ], style={'backgroundColor': 'white', 'maxWidth': '1000px', 'margin': '0 auto'})
