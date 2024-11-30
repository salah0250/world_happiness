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
    
    def create_country_trends(self, regions=None, countries=None):
        # Calculate global min and max values for the Y-axis
        global_min = self.data['Happiness Score'].min() - 0.5
        global_max = self.data['Happiness Score'].max() + 0.5

        # Filter data based on selected regions
        if regions:
            filtered_data = self.data[self.data['Region'].isin(regions)]
        else:
            filtered_data = self.data

        # Filter data based on selected countries
        if countries:
            filtered_data = filtered_data[filtered_data['Country'].isin(countries)]

        # Group by country and year
        country_insights = filtered_data.groupby(['Country', 'Year', 'Region'])['Happiness Score'].mean().reset_index()

        # Filter years to 2015 to 2019
        country_insights = country_insights[country_insights['Year'].between(2015, 2019)]

        # Ensure 'Year' is integer type
        country_insights['Year'] = country_insights['Year'].astype(int)

        # Create a color mapping for regions
        unique_regions = country_insights['Region'].unique()
        color_map = {region: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, region in
                     enumerate(unique_regions)}

        # Apply color mapping to countries based on their regions
        country_insights['Color'] = country_insights['Region'].map(color_map)

        # Create line plot with markers
        fig = px.line(
            country_insights,
            x='Year',
            y='Happiness Score',
            color='Country',
            title='Country Happiness Trends',
            markers=True,
            hover_data = {'Region': True}
        )

        # Update traces to use the color mapping
        for trace in fig.data:
            country = trace.name
            region = country_insights[country_insights['Country'] == country]['Region'].values[0]
            trace.line.color = color_map[region]

        fig.update_layout(
            template='plotly_white',
            xaxis=dict(
                tickmode='linear',
                dtick=1,
                tickformat='d',
                range=[2014.8, 2019.2]
            ),
            yaxis=dict(
                range=[global_min, global_max],
                dtick=0.5,
                tickformat='d',
                tickvals=[i for i in range(int(global_min), int(global_max) + 1)],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            legend_title_text='Country',
            height=600
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
        # If no countries selected or more than 3 countries, return empty figure
        if not countries:
            return go.Figure()

        # Limit to 3 countries maximum
        countries = countries[:3]

        # Prepare the figure
        fig = go.Figure()

        # Custom color palette
        colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3',
                  '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd']

        # Calculate domain positions with spacing
        chart_width = 0.25  # Width of each pie chart
        spacing = 0.1  # Space between charts
        total_width = len(countries) * chart_width + (len(countries) - 1) * spacing
        start_pos = (1 - total_width) / 2  # Center the charts horizontally

        # Add pie charts for selected countries
        for i, country in enumerate(countries):
            # Filter data for specific country and year
            country_data = self.data[(self.data['Country'] == country) & (self.data['Year'] == year)]

            if not country_data.empty:
                # Extract happiness factors
                factors = ['Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                           'Freedom', 'Trust (Government Corruption)', 'Generosity']
                values = country_data[factors].values[0]

                # Calculate position for current pie chart
                x_start = start_pos + i * (chart_width + spacing)
                x_end = x_start + chart_width

                # Add pie chart
                fig.add_trace(go.Pie(
                    labels=factors,
                    values=values,
                    name=country,
                    title=f"{country} - ({year})",
                    domain={'x': [x_start, x_end]},
                    marker=dict(colors=colors),
                    hoverinfo='label+percent+name'
                ))

        # Update layout to show all pie charts side by side
        fig.update_layout(
            title=f"Happiness Factors Breakdown - {year} (Max 3 Countries)",
            showlegend=True,
            height=500,
            margin=dict(t=50, b=50, l=50, r=50)
        )

        return fig