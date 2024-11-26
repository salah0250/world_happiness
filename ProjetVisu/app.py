import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go  # Importer plotly.graph_objects
from plotly.subplots import make_subplots  # Importer make_subplots
import dash_bootstrap_components as dbc

# Construire le chemin relatif pour charger les données
file_path = os.path.join("data", "happiness_info.csv")
data = pd.read_csv(file_path)

# Initialiser l'application Dash avec un thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Définir la palette de couleurs personnalisée
custom_colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd"]

# Fonction pour créer la carte
def create_map_figure(region_filter, happiness_range, country_filter, year):
    filtered_data = data[(data['Happiness Score'] >= happiness_range[0]) & (data['Happiness Score'] <= happiness_range[1])]
    if region_filter:
        filtered_data = filtered_data[filtered_data['Region'].isin(region_filter)]
    if country_filter:
        filtered_data = filtered_data[filtered_data['Country'].isin(country_filter)]
    if year:
        filtered_data = filtered_data[filtered_data['Year'] == year]

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
        color_continuous_scale=px.colors.sequential.Plasma[::-1],  # Inverser la palette de couleurs
        title="Distribution Mondiale du Bonheur par Pays",
        labels={'Happiness Score': 'Score de Bonheur'},
        animation_frame="Year"  # Ajouter l'animation par année
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        coloraxis_colorbar=dict(
            title="Score de Bonheur",
            len=0.6
        )
    )

    return fig

# Layout de l'application
# Layout de l'application
app.layout = dbc.Container([
    html.H1("Tableau de Bord Interactif du Bonheur Mondial", style={'text-align': 'center', 'color': 'darkblue'}),

    # La carte prend toute la largeur
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='map', style={'width': '100%', 'height': '70vh'}),
            width=12  # Prend toute la ligne
        ),
    ], style={'margin-bottom': '20px'}),  # Ajouter un espacement en bas

    # Filtres (Dropdowns, RangeSlider, etc.)
    dbc.Row([
        dbc.Col([
            html.Label("Choisir l'année :"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(year), "value": year} for year in data["Year"].unique()],
                value=data["Year"].min(),
                placeholder="Sélectionnez une année"
            ),
            html.Label("Filtrer par Région :"),
            dcc.Dropdown(
                id="region-dropdown",
                options=[{"label": region, "value": region} for region in data["Region"].unique()],
                multi=True,
                placeholder="Sélectionnez une ou plusieurs régions"
            ),
            html.Label("Filtrer par Pays :"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": country, "value": country} for country in data["Country"].unique()],
                multi=True,
                placeholder="Sélectionnez un ou plusieurs pays"
            ),
            html.Label("Filtrer par Score de Bonheur :"),
            dcc.RangeSlider(
                id="happiness-range",
                min=data['Happiness Score'].min(),
                max=data['Happiness Score'].max(),
                step=0.5,
                value=[data['Happiness Score'].min(), data['Happiness Score'].max()],
                marks={i: str(i) for i in range(int(data['Happiness Score'].min()), int(data['Happiness Score'].max()) + 1)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Checklist(
                id="trendline-checkbox",
                options=[{"label": "Afficher la ligne de tendance", "value": "trendline"}],
                value=[]
            )
        ], width=3),  # Largeur pour les filtres
    ], style={'margin-bottom': '20px'}),

    # Les autres visualisations : deux colonnes par ligne
    dbc.Row([
        dbc.Col(dcc.Graph(id="scatter-plot"), width=6),  # Première visualisation
        dbc.Col(dcc.Graph(id="bar-chart"), width=6)     # Deuxième visualisation
    ], style={'margin-bottom': '20px'}),  # Espacement entre les lignes

    dbc.Row([
        dbc.Col(dcc.Graph(id="line-chart"), width=6),  # Troisième visualisation
        dbc.Col(dcc.Graph(id="pie-chart"), width=6)    # Quatrième visualisation
    ])
])


# Callback combiné
@app.callback(
    [Output("scatter-plot", "figure"),
     Output("bar-chart", "figure"),
     Output("line-chart", "figure"),
     Output("map", "figure")],
    [Input("year-dropdown", "value"),
     Input("region-dropdown", "value"),
     Input("country-dropdown", "value"),
     Input("trendline-checkbox", "value"),
     Input("map", "clickData")],
    [State("happiness-range", "value")]
)
def update_all_charts(selected_year, selected_regions, selected_countries, show_trendline, clickData, happiness_range):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Initialiser `countries` si vide
    if not selected_countries:
        selected_countries = []

    # Ajouter ou retirer un pays en fonction des clics sur la carte
    if trigger_id == 'map' and clickData:
        clicked_country = clickData['points'][0]['location']
        if clicked_country in selected_countries:
            selected_countries = [c for c in selected_countries if c != clicked_country]
        else:
            selected_countries.append(clicked_country)

    # Filtrer les données
    filtered_data = data[(data["Year"] == selected_year) &
                         (data['Happiness Score'] >= happiness_range[0]) &
                         (data['Happiness Score'] <= happiness_range[1])]

    if selected_regions:
        filtered_data = filtered_data[filtered_data["Region"].isin(selected_regions)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data["Country"].isin(selected_countries)]

    # Mise à jour des graphiques
    scatter_plot = px.scatter(
        filtered_data,
        x="Economy (GDP per Capita)",
        y="Happiness Score",
        color="Region",
        hover_name="Country",
        title=f"Corrélation entre le PIB et le Bonheur - Année {selected_year}"
    )

    bar_chart = px.bar(
        filtered_data,
        x="Country",
        y="Happiness Score",
        color="Region",
        title=f"Scores de Bonheur par Pays - Année {selected_year}"
    )

    # Créer le graphique en ligne
    line_chart_data = data[
        (data['Happiness Score'] >= happiness_range[0]) &
        (data['Happiness Score'] <= happiness_range[1])
        ]
    if selected_regions:
        line_chart_data = line_chart_data[line_chart_data["Region"].isin(selected_regions)]
    if selected_countries:
        line_chart_data = line_chart_data[line_chart_data["Country"].isin(selected_countries)]
    if not selected_regions and not selected_countries:
        default_countries = ["Switzerland", "Denmark", "Norway", "Canada"]
        line_chart_data = line_chart_data[line_chart_data["Country"].isin(default_countries)]
    if not line_chart_data.empty:
        line_chart = px.line(
            line_chart_data,
            x="Year",
            y="Happiness Score",
            color="Country",
            title="Évolution du Score de Bonheur pour les Pays Sélectionnés"
        )
        line_chart.update_layout(
            template="plotly_white",
            xaxis=dict(tickmode='linear', tick0=data["Year"].min(), dtick=1)
        )
    else:
        line_chart = px.line(title="Aucune donnée disponible pour les filtres sélectionnés")

    map_figure = create_map_figure(selected_regions, happiness_range, selected_countries, selected_year)

    return scatter_plot, bar_chart, line_chart, map_figure


@app.callback(
    Output("country-dropdown", "options"),
    [Input("region-dropdown", "value")]
)
def update_country_options(selected_regions):
    # Si des régions sont sélectionnées, limiter les pays à ces régions
    if selected_regions:
        filtered_data = data[data["Region"].isin(selected_regions)]
        country_options = [{"label": country, "value": country} for country in filtered_data["Country"].unique()]
    else:
        # Si aucune région n'est sélectionnée, afficher tous les pays
        country_options = [{"label": country, "value": country} for country in data["Country"].unique()]
    return country_options




# Callback pour mettre à jour le graphique en camembert avec sous-graphiques
@app.callback(
    Output("pie-chart", "figure"),
    [Input("country-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_pie_chart(selected_countries, selected_year):
    # Si aucun pays n'est sélectionné, ne rien afficher
    if not selected_countries:
        return go.Figure()

    # Créer une figure avec des sous-graphiques de type 'domain' pour chaque pays sélectionné
    fig = make_subplots(
        rows=1, cols=len(selected_countries),
        specs=[[{"type": "domain"}] * len(selected_countries)],
        subplot_titles=selected_countries
    )

    # Boucle sur chaque pays sélectionné
    for i, country in enumerate(selected_countries, 1):
        # Filtrer les données pour le pays et l'année sélectionnés
        filtered_data = data[(data["Country"] == country) & (data["Year"] == selected_year)]

        # Vérifier si des données sont disponibles pour le pays et l'année
        if not filtered_data.empty:
            factors = filtered_data.iloc[0]  # Première ligne pour le pays sélectionné
            factors_data = factors[['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 'Freedom',
                                    'Trust (Government Corruption)', 'Generosity']]

            # Ajouter un camembert pour chaque pays en tant que sous-graphe
            fig.add_trace(
                go.Pie(
                    labels=factors_data.index,
                    values=factors_data,
                    name=country,
                    marker=dict(colors=custom_colors)
                ),
                row=1, col=i
            )

    # Mettre à jour le layout de la figure
    fig.update_layout(
        title=f"Répartition des Facteurs de Bonheur pour les Pays Sélectionnés en {selected_year}",
        showlegend=True
    )

    return fig


# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)