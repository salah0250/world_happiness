import dash_bootstrap_components as dbc
from dash import html

def create_info_cards(dashboard):
    # Calculate global statistics
    global_stats = {
        'total_countries': len(dashboard.data['Country'].unique()),
        'avg_happiness': round(dashboard.data['Happiness Score'].mean(), 2),
        'top_region': dashboard.regional_insights.groupby('Region')['Happiness Score'].mean().idxmax(),
        'recent_year': dashboard.data['Year'].max()
    }
    
    return dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Total Countries"),
                dbc.CardBody([
                    html.H6(global_stats['total_countries'], className="text-primary"),
                    html.P("Nations analyzed", className="text-muted")
                ])
            ], className="text-center mb-3"),
            width=3
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Average Happiness"),
                dbc.CardBody([
                    html.H6(f"{global_stats['avg_happiness']}/10", className="text-success"),
                    html.P("Global Happiness Score", className="text-muted")
                ])
            ], className="text-center mb-3"),
            width=3
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Performing Region"),
                dbc.CardBody([
                    html.H6(global_stats['top_region'], className="text-info"),
                    html.P("Happiest Region", className="text-muted")
                ])
            ], className="text-center mb-3"),
            width=3
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Latest Data"),
                dbc.CardBody([
                    html.H6(global_stats['recent_year'], className="text-warning"),
                    html.P("Most Recent Year", className="text-muted")
                ])
            ], className="text-center mb-3"),
            width=3
        )
    ], className="mb-4")