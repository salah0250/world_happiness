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
        dcc.Graph(id="scatter-plot")
    ], style={"width": "70%", "display": "inline-block", "padding": "0 20px"})
])


# Callback pour mettre à jour le graphique
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
            hover_name="Country",
            title=f"Corrélation entre le PIB et le Bonheur - Année {selected_year}",
            trendline="ols"
        )

    fig.update_layout(template="plotly_white")
    return fig


# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
