import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the data
data = pd.read_csv('data/happiness_info.csv')

# Options for filtering by region
regions = data['Region'].unique()
regions_options = [{'label': region, 'value': region} for region in regions]

# Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the map figure
def create_map_figure(region_filter, happiness_range):
    filtered_data = data[(data['Happiness Score'] >= happiness_range[0]) & 
                         (data['Happiness Score'] <= happiness_range[1])]
    if region_filter:
        filtered_data = filtered_data[filtered_data['Region'].isin(region_filter)]

    fig = px.choropleth(
        filtered_data,
        locations="Country",
        locationmode="country names",
        color="Happiness Score",
        hover_name="Country",
        hover_data={
            "Happiness Score": True,
            "Region": True,
            "Economy (GDP per Capita)": True,
            "Health (Life Expectancy)": True
        },
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Distribution Mondiale du Bonheur par Pays",
        labels={'Happiness Score': 'Score de Bonheur'}
    )

    fig.update_layout(
        title=dict(
            text="Distribution Mondiale du Bonheur par Pays",
            x=0.5,
            xanchor='center',
            font=dict(size=24, color="darkblue")
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        coloraxis_colorbar=dict(
            title="Score de Bonheur",
            tickvals=[2, 4, 6, 8, 10],
            ticktext=["Très Bas", "Bas", "Moyen", "Élevé", "Très Élevé"],
            len=0.6
        )
    )

    return fig

# Create the country figure
def create_country_figure(country):
    country_data = data[data['Country'] == country]

    indicators = ['Happiness Score', 'Economy (GDP per Capita)', 'Health (Life Expectancy)', 'Freedom']
    y_values = country_data.iloc[0, [data.columns.get_loc(ind) for ind in indicators]].values

    fig = px.bar(
        x=indicators,
        y=y_values,
        title=f"Indicateurs du Bonheur pour {country}",
        labels={'x': 'Indicateur', 'y': 'Valeur'}
    )

    return fig

# Layout of the application
app.layout = dbc.Container([
    html.H1("Tableau de Bord Interactif du Bonheur Mondial", style={'text-align': 'center', 'color': 'darkblue'}),
    
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Label("Filtrer par Région:", style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='region-filter',
                        options=regions_options,
                        multi=True,
                        placeholder="Sélectionnez une ou plusieurs régions",
                        style={'width': '100%'}
                    )
                ])
            ], style={'margin-bottom': '20px'}),
            width=5
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Label("Filtrer par Score de Bonheur:", style={'font-weight': 'bold'}),
                    dcc.RangeSlider(
                        id='happiness-range',
                        min=data['Happiness Score'].min(),
                        max=data['Happiness Score'].max(),
                        step=0.5,
                        value=[data['Happiness Score'].min(), data['Happiness Score'].max()],
                        marks={i: str(i) for i in range(int(data['Happiness Score'].min()), int(data['Happiness Score'].max())+1)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ])
            ], style={'margin-bottom': '20px'}),
            width=7
        )
    ], style={'margin-bottom': '20px'}),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='map', style={'width': '100%', 'height': '70vh'})
                ])
            ], style={'margin-bottom': '20px'}),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='country-info', style={'text-align': 'center', 'margin-top': '20px'})
                ])
            ]),
            width=12
        )
    ])
])

# Update the map based on filters
@app.callback(
    Output('map', 'figure'),
    [Input('region-filter', 'value'),
     Input('happiness-range', 'value')])
def update_map(region_filter, happiness_range):
    return create_map_figure(region_filter, happiness_range)

# Display details of the selected country
@app.callback(
    Output('country-info', 'children'),
    [Input('map', 'clickData')])
def display_country_info(clickData):
    if clickData:
        country = clickData['points'][0]['location']
        return dcc.Graph(figure=create_country_figure(country))
    return "Cliquez sur un pays pour voir plus d'informations."

if __name__ == '__main__':
    app.run_server(debug=True)
