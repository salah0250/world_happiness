import dash_bootstrap_components as dbc
from dash import html

def create_help_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("Help & Guide"),
            dbc.ModalBody([
                html.H4("How to Use the Dashboard"),
                html.Ul([
                    html.Li("Select a year to view data for that specific year"),
                    html.Li("Use region and country dropdowns to filter your view"),
                    html.Li("Adjust the happiness range slider to focus on specific happiness levels"),
                    html.Li("Hover over graphs for more detailed information"),
                    html.Li("Click on map elements for country-specific details")
                ]),
                html.H4("Understanding the Metrics"),
                html.P("""
                    The Happiness Score is calculated based on multiple factors including 
                    GDP per capita, social support, healthy life expectancy, freedom to make 
                    life choices, generosity, and perceptions of corruption.
                """)
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-help-modal", className="ml-auto")
            )
        ],
        id="help-modal",
        size="lg",
        centered=True
    )

def create_about_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader("About Global Happiness Explorer"),
            dbc.ModalBody([
                html.H4("Our Mission"),
                html.P("""
                    We aim to provide comprehensive insights into global happiness, 
                    helping people understand the complex factors that contribute 
                    to well-being across different countries and regions.
                """),
                html.H4("Data Source"),
                html.P("""
                    Our data is sourced from the World Happiness Report, an annual 
                    publication by the United Nations Sustainable Development Solutions Network.
                """),
                html.H4("Key Contributors"),
                html.Ul([
                    html.Li("Data Analysis Team"),
                    html.Li("Visualization Experts"),
                    html.Li("User Experience Designers")
                ])
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-about-modal", className="ml-auto")
            )
        ],
        id="about-modal",
        size="lg",
        centered=True
    )