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
            value=[data["Region"].unique()[0]],  # Valeur par défaut : une seule région sélectionnée
            multi=True
        ),

        html.Label("Choisir le pays :"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": country, "value": country} for country in data["Country"].unique()],
            value=[data["Country"].unique()[0]],  # Valeur par défaut : un seul pays sélectionné
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
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="line-chart")
    ], style={"width": "70%", "display": "inline-block", "padding": "0 20px"})
])

# Callback pour mettre à jour le graphique en barres
@app.callback(
    Output("bar-chart", "figure"),
    [Input("year-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_bar_chart(selected_year, selected_regions):
    filtered_data = data[(data["Year"] == selected_year) & (data["Region"].isin(selected_regions))]
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
def update_scatter_plot(selected_year, selected_regions, show_trendline):
    filtered_data = data[(data["Year"] == selected_year) & (data["Region"].isin(selected_regions))]
    fig = px.scatter(
        filtered_data,
        x="Economy (GDP per Capita)",
        y="Happiness Score",
        color="Region",
        color_discrete_sequence=custom_colors,
        hover_name="Country",
        title=f"Corrélation entre le PIB et le Bonheur - Année {selected_year}"
    )
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

# Callback pour mettre à jour le graphique en lignes
@app.callback(
    Output("line-chart", "figure"),
    [Input("country-dropdown", "value"),
     Input("region-dropdown", "value")]
)
def update_line_chart(selected_countries, selected_regions):
    filtered_data = data[(data["Country"].isin(selected_countries)) | (data["Region"].isin(selected_regions))]
    fig = px.line(
        filtered_data,
        x="Year",
        y="Happiness Score",
        color="Country",
        color_discrete_sequence=custom_colors,
        title="Évolution du Score de Bonheur pour les Pays et Régions Sélectionnés"
    )
    fig.update_layout(template="plotly_white")
    return fig

# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
