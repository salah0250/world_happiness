import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Construire le chemin relatif
file_path = os.path.join("data", "happiness_info.csv")

# Charger les données
data = pd.read_csv(file_path)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Définir la palette de couleurs personnalisée
custom_colors = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd"]

# Layout de l'application
app.layout = html.Div([
    html.H1("Tableau de Bord - Corrélation entre PIB et Bonheur"),

    html.Div([
        html.Label("Choisir l'année :"),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": str(year), "value": year} for year in data["Year"].unique()],
            value=data["Year"].min()
        ),

        html.Label("Choisir la région :"),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": region, "value": region} for region in data["Region"].unique()],
            value=data["Region"].unique().tolist(),  # Valeur par défaut : toutes les régions
            multi=True
        ),

        dcc.Checklist(
            id="trendline-checkbox",
            options=[{"label": "Afficher la ligne de tendance", "value": "trendline"}],
            value=[]
        )
    ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        dcc.Graph(id="scatter-plot"),
        dcc.Graph(id="bar-chart")  # Nouveau graphique en barres
    ], style={"width": "70%", "display": "inline-block", "padding": "0 20px"})
])

# Callback pour mettre à jour le graphique en barres
@app.callback(
    Output("bar-chart", "figure"),
    [Input("year-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_bar_chart(selected_year, selected_regions):
    # Filtrer les données en fonction de l'année et des régions sélectionnées
    filtered_data = data[(data["Year"] == selected_year) & (data["Region"].isin(selected_regions))]

    # Créer le graphique en barres
    fig = px.bar(
        filtered_data,
        x="Country",
        y="Happiness Score",
        color="Region",
        color_discrete_sequence=custom_colors,
        title=f"Scores de Bonheur par Pays - Année {selected_year}"
    )

    fig.update_layout(template="plotly_white")
    return fig

# Callback pour mettre à jour le graphique en nuage de points
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("year-dropdown", "value"),
     Input("region-dropdown", "value"),
     Input("trendline-checkbox", "value")]
)
def update_graph(selected_year, selected_regions, show_trendline):
    # Filtrer les données en fonction de l'année et des régions sélectionnées
    filtered_data = data[(data["Year"] == selected_year) & (data["Region"].isin(selected_regions))]

    # Créer le graphique
    fig = px.scatter(
        filtered_data,
        x="Economy (GDP per Capita)",
        y="Happiness Score",
        color="Region",
        color_discrete_sequence=custom_colors,
        hover_name="Country",
        title=f"Corrélation entre le PIB et le Bonheur - Année {selected_year}"
    )

    # Ajouter une ligne de tendance si l'option est cochée
    if "trendline" in show_trendline:
        fig = px.scatter(
            filtered_data,
            x="Economy (GDP per Capita)",
            y="Happiness Score",
            color="Region",
            color_discrete_sequence=custom_colors,
            hover_name="Country",
            title=f"Corrélation entre le PIB et le Bonheur - Année {selected_year}",
            trendline="ols"
        )

    fig.update_layout(template="plotly_white")
    return fig

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)