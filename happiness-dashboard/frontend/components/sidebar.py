import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

def create_sidebar(dashboard):
    return dbc.Card([
        dbc.CardHeader(
            html.Div(
                [
                    html.H4(
                        [
                            html.I(
                                className="fas fa-filter me-2", 
                                id="filter-toggle-icon",
                                style={
                                    'cursor': 'pointer',
                                    'transition': 'transform 0.3s ease'
                                }
                            ),
                            "Filters"
                        ], 
                        className="text-center d-flex justify-content-between align-items-center"
                    )
                ]
            )
        ),
        dbc.Collapse(
            dbc.CardBody([
                # Year Selector
                html.Label(
                    ["Select Year", html.Span(" 🕒", className="ms-2")], 
                    className="font-weight-bold animate__animated animate__slideInLeft"
                ),
                dcc.Dropdown(
                    id='year-selector',
                    options=dashboard.get_year_options(),
                    value=dashboard.data['Year'].max(),
                    clearable=False,
                    className="mb-3 dropdown-animated"
                ),
                
                # Region Selector
                html.Label(
                    ["Select Regions", html.Span(" 🌍", className="ms-2")], 
                    className="font-weight-bold animate__animated animate__slideInRight"
                ),
                dcc.Dropdown(
                    id='region-selector',
                    options=dashboard.get_region_options(),
                    multi=True,
                    placeholder="All Regions",
                    className="mb-3 dropdown-animated"
                ),
                
                # Country Selector
                html.Label(
                    ["Select Countries", html.Span(" 🚩", className="ms-2")], 
                    className="font-weight-bold animate__animated animate__slideInLeft"
                ),
                dcc.Dropdown(
                    id='country-selector',
                    options=dashboard.get_country_options(),
                    multi=True,
                    placeholder="All Countries",
                    className="mb-3 dropdown-animated"
                ),
                
                # Happiness Range Slider
                html.Label(
                    ["Happiness Range", html.Span(" 😊", className="ms-2")], 
                    className="font-weight-bold animate__animated animate__slideInRight"
                ),
                dcc.RangeSlider(
                    id='happiness-range',
                    min=dashboard.data['Happiness Score'].min(),
                    max=dashboard.data['Happiness Score'].max(),
                    step=0.1,
                    marks={i: str(i) for i in range(
                        int(dashboard.data['Happiness Score'].min()), 
                        int(dashboard.data['Happiness Score'].max())+1
                    )},
                    value=[
                        dashboard.data['Happiness Score'].min(), 
                        dashboard.data['Happiness Score'].max()
                    ],
                    className="mb-4 range-slider-animated"
                ),
                
                # Advanced Filter Button
                dbc.Button(
                    [
                        html.I(className="fas fa-cog me-2"),
                        "Advanced Filters"
                    ], 
                    id="advanced-filters-toggle", 
                    color="secondary", 
                    className="w-100 btn-hover-effect"
                )
            ]),
            id="filter-collapse",
            is_open=True,
        )
    ], className="sidebar-filter")

def create_menu_sidebar():
    return dbc.Nav(
        [
            # Sidebar Links
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fas fa-chart-pie me-2"), "Radar Chart"], 
                        href="/radar-chart", 
                        className="nav-link sidebar-nav-item text-light",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-chart-line me-2"), ""], 
                        href="/", 
                        className="nav-link sidebar-nav-item text-light",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-user me-2"), ""], 
                        href="/", 
                        className="nav-link sidebar-nav-item text-light",
                        active="exact"
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-cogs me-2"), ""], 
                        href="/", 
                        className="nav-link sidebar-nav-item text-light",
                        active="exact"
                    ),
                ],
                vertical=True,
                pills=True,
                className="flex-column sidebar-nav-container mt-3"
            ),
        ],
        id="menu-sidebar",
        className="sidebar-menu bg-dark",
        style={
            'position': 'fixed',
            'left': '0',
            'top': '0',
            'bottom': '0',
            'width': '250px',
            'padding': '20px 10px',
            'overflowY': 'auto',
            'zIndex': '1030',
            'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
            'transition': 'transform 0.3s ease-in-out',
            'transform': 'translateX(-100%)'
        }
    )
