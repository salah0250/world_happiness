import dash_bootstrap_components as dbc
from dash import html

def create_header():
    return dbc.Navbar(
        dbc.Container([
            # Animated Logo and Brand with Hover Effect
            dbc.Row([
                dbc.Col([
                    html.Span(
                        [
                            html.I(className="fas fa-globe me-2"),  # Font Awesome Globe Icon
                            "Global Happiness Explorer"
                        ],
                        className='navbar-brand animate__animated animate__pulse animate__slow',
                        style={
                            'transition': 'color 0.3s ease',
                            'cursor': 'pointer'
                        },
                        id='brand-logo'
                    )
                ])
            ]),
            
            # Navigation Links with Hover Animations
            dbc.Nav([
                dbc.NavItem(
                    dbc.Button(
                        [
                            html.I(className="fas fa-bars me-2"),
                            "Menu"
                        ],
                        color="secondary", 
                        className="ml-2 btn-hover-effect",
                        id="menu-button"
                    )
                )
            ], navbar=True)
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4 navbar-animated"
    )


