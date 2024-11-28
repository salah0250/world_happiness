import dash_bootstrap_components as dbc
from dash import dcc, html
from frontend.components.header import create_header
from frontend.components.sidebar import create_sidebar
from frontend.components.info_cards import create_info_cards
from frontend.components.modals import create_help_modal
from frontend.components.sidebar import create_menu_sidebar
def create_layout(dashboard):
    return dbc.Container([
        create_header(),
        create_menu_sidebar(),
        dbc.Row([
            dbc.Col(create_sidebar(dashboard), width=3),
            dbc.Col([
                create_info_cards(dashboard),
                dcc.Graph(id='world-map'),
                dcc.Graph(id='scatter-plot'),
                dcc.Graph(id='bar-chart'),
                dcc.Graph(id='pie-chart'),
                dcc.Graph(id='regional-trends'),
            ], width=9)
        ]),
        create_help_modal()
    ], fluid=True)