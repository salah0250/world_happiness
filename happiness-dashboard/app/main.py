import dash
import dash_bootstrap_components as dbc
from app.data_processor import HappinessDashboard
from app.visualizations import create_layout
from app.callbacks import register_callbacks
from app.callbacks import register_sidebar_toggle_callback

def create_dash_app():
    # Initialize the Dash app with Bootstrap theme
    app = dash.Dash(
        __name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME , '../frontend/assets/animate.min.css'],
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )
    register_sidebar_toggle_callback(app)


    # Set the app title
    app.title = "Global Happiness Explorer"

    # Initialize the dashboard
    dashboard = HappinessDashboard('data/happiness_info.csv')

    # Create the layout
    app.layout = create_layout(dashboard)

    # Register callbacks
    register_callbacks(app, dashboard)

    return app