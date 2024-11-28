import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

class HappinessDashboard:
    def __init__(self, data_path):
        # Load and preprocess data
        self.data = pd.read_csv(data_path)
        self.prepare_data()
    
    def prepare_data(self):
        # Normalize happiness scores
        self.data['Normalized Happiness'] = (self.data['Happiness Score'] - self.data['Happiness Score'].min()) / \
                                            (self.data['Happiness Score'].max() - self.data['Happiness Score'].min())
        
        # Calculate global and regional trends
        self.global_trends = self.data.groupby('Year')['Happiness Score'].mean().reset_index()
        self.regional_insights = self.data.groupby(['Region', 'Year'])['Happiness Score'].mean().reset_index()
    
    def get_year_options(self):
        return [{'label': str(year), 'value': year} for year in sorted(self.data['Year'].unique())]
    
    def get_region_options(self):
        return [{'label': region, 'value': region} for region in sorted(self.data['Region'].unique())]
    
    def get_country_options(self, regions=None):
        if regions:
            filtered_countries = self.data[self.data['Region'].isin(regions)]['Country'].unique()
        else:
            filtered_countries = self.data['Country'].unique()
        return [{'label': country, 'value': country} for country in sorted(filtered_countries)]
    
    def create_world_map(self, year, regions=None, countries=None):
        # Filter data
        filtered_data = self.data[self.data['Year'] == year].copy()
        
        if regions:
            filtered_data = filtered_data[filtered_data['Region'].isin(regions)]
        if countries:
            filtered_data = filtered_data[filtered_data['Country'].isin(countries)]
        
        # Create choropleth map
        fig = px.choropleth(
            filtered_data,
            locations="Country",
            locationmode="country names",
            color="Normalized Happiness",
            hover_name="Country",
            hover_data={
                "Happiness Score": ":.2f",
                "Region": True,
                "Economy (GDP per Capita)": ":.2f",
            },
            color_continuous_scale='viridis',
            title=f"Global Happiness Distribution {year}"
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False, 
                showcoastlines=True, 
                projection_type='natural earth'
            ),
            coloraxis_colorbar=dict(
                title="Normalized Happiness",
                len=0.6
            )
        )
        
        return fig
    
    def create_scatter_plot(self, year, regions=None, countries=None):
            # Calculer les valeurs globales de min et max pour l'axe Y
        global_min = self.data['Happiness Score'].min()
        global_max = self.data['Happiness Score'].max()

        # Filter data
        filtered_data = self.data[self.data['Year'] == year].copy()
        
        if regions:
            filtered_data = filtered_data[filtered_data['Region'].isin(regions)]
        if countries:
            filtered_data = filtered_data[filtered_data['Country'].isin(countries)]
        
        # Create scatter plot
        fig = px.scatter(
            filtered_data, 
            x="Economy (GDP per Capita)", 
            y="Happiness Score",
            color="Region",
            size="Health (Life Expectancy)",
            hover_name="Country",
            hover_data={
                "Economy (GDP per Capita)": ":.2f",
                "Health (Life Expectancy)": ":.2f",
                "Freedom": ":.2f"
            },
            title=f"Happiness Ecosystem - {year}"
        )
        
        fig.update_layout(template='plotly_white',
              yaxis=dict(
            # Fixer l'échelle avec les valeurs globales min et max
            range=[0, 8],
            # Ajouter des lignes de grille pour une meilleure lisibilité
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )             )
        
        return fig
    
    def create_regional_trends(self, regions=None):
    # Calculer les valeurs globales de min et max pour l'axe Y
     global_min = self.data['Happiness Score'].min()
     global_max = self.data['Happiness Score'].max()

    # Filter regional insights
     if regions:
        filtered_insights = self.regional_insights[self.regional_insights['Region'].isin(regions)]
     else:
        filtered_insights = self.regional_insights
    
    # Create line plot
     fig = px.line(
        filtered_insights, 
        x='Year', 
        y='Happiness Score', 
        color='Region',
        title='Regional Happiness Trends'
     )
    
     fig.update_layout(
        template='plotly_white',
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis=dict(
            # Fixer l'échelle avec les valeurs globales min et max
            range=[global_min, global_max],
            # Ajouter des lignes de grille pour une meilleure lisibilité
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
     )
    
     return fig
    def create_bar_chart(self, year, regions=None, countries=None):
     # Filter data
     filtered_data = self.data[self.data['Year'] == year].copy()
    
     if regions:
        filtered_data = filtered_data[filtered_data['Region'].isin(regions)]
     if countries:
        filtered_data = filtered_data[filtered_data['Country'].isin(countries)]
    
     # Sort countries by happiness score in descending order
     filtered_data = filtered_data.sort_values('Happiness Score', ascending=False)
    
     # Create bar chart
     fig = px.bar(
        filtered_data, 
        x="Country", 
        y="Happiness Score",
        color="Region",
        title=f"Happiness Scores by Country - {year}",
        hover_data={
            "Economy (GDP per Capita)": ":.2f",
            "Health (Life Expectancy)": ":.2f",
            "Freedom": ":.2f"
        }
     )
    
     fig.update_layout(
        template='plotly_white',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability,
         yaxis=dict(
            # Fixer l'échelle avec les valeurs globales min et max
            range=[0, 8],
            # Ajouter des lignes de grille pour une meilleure lisibilité
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
     )
    
     return fig

    def create_pie_chart(self, year, countries=None):
     # Si aucun pays n'est sélectionné ou plus de 4 pays, retournez un message ou un graphique vide
     if not countries:
         return go.Figure()
     
     # Limiter à 4 pays maximum
     countries = countries[:4]
    
     # Prepare the figure
     fig = go.Figure()
    
     # Custom color palette
     colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', 
              '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd']
    
    # Add pie charts for selected countries
     for i, country in enumerate(countries):
        # Filter data for specific country and year
        country_data = self.data[(self.data['Country'] == country) & (self.data['Year'] == year)]
        
        if not country_data.empty:
            # Extract happiness factors
            factors = ['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
                       'Freedom', 'Trust (Government Corruption)', 'Generosity']
            values = country_data[factors].values[0]
            
            # Add pie chart
            fig.add_trace(go.Pie(
                labels=factors,
                values=values,
                name=country,
                title=f"{country} - ({year})",
                domain={'x': [i/len(countries), (i+1)/len(countries)]}
            ))
    
     # Update layout to show all pie charts side by side
     fig.update_layout(
        title=f"Happiness Factors Breakdown - {year} (Max 4 Countries)",
        showlegend=True,
        height=500
     )
    
     return fig