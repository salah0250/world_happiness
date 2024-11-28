from dash.dependencies import Input, Output , State,  MATCH
from dash import callback, Input, Output, State

def register_callbacks(app, dashboard):
    @app.callback(
        [Output('world-map', 'figure'),
         Output('scatter-plot', 'figure'),
         Output('regional-trends', 'figure'),
         Output('bar-chart', 'figure'),
         Output('pie-chart', 'figure'),
         Output('country-selector', 'options')],
        [Input('year-selector', 'value'),
         Input('region-selector', 'value'),
         Input('country-selector', 'value'),
         Input('happiness-range', 'value')]
    )
    def update_dashboard(year, regions, countries, happiness_range):
        # Start with the full dataset
        filtered_data = dashboard.data.copy()
        
        # Filter data based on happiness range
        filtered_data = filtered_data[
            (filtered_data['Happiness Score'] >= happiness_range[0]) & 
            (filtered_data['Happiness Score'] <= happiness_range[1])
        ]
        
        # Filter by year
        filtered_data = filtered_data[filtered_data['Year'] == year]
        
        # Filter by regions if specified
        if regions:
            filtered_data = filtered_data[filtered_data['Region'].isin(regions)]
        
        # Update country options based on current filters
        country_options = dashboard.get_country_options(regions)
        
        # If countries are specified, use them; otherwise, use all filtered countries
        selected_countries = countries if countries else filtered_data['Country'].unique().tolist()
        
        # Create visualizations
        world_map = dashboard.create_world_map(year, regions, selected_countries)
        scatter_plot = dashboard.create_scatter_plot(year, regions, selected_countries)
        regional_trends = dashboard.create_regional_trends(regions)
        bar_chart = dashboard.create_bar_chart(year, regions, selected_countries)
        pie_chart = dashboard.create_pie_chart(year, selected_countries)
        
        return world_map, scatter_plot, regional_trends, bar_chart, pie_chart, country_options

    @app.callback(
        Output('region-selector', 'value'),
        [Input('country-selector', 'value')],
        [State('region-selector', 'value')]
    )
    def update_regions_based_on_countries(selected_countries, current_regions):
        if not selected_countries:
            return current_regions

        # Get regions of selected countries
        selected_regions = dashboard.data[dashboard.data['Country'].isin(selected_countries)]['Region'].unique().tolist()

        # Combine current regions with new regions
        if current_regions:
            selected_regions = list(set(current_regions + selected_regions))

        return selected_regions
    @app.callback(
    Output('country-selector', 'value'),
    [Input('world-map', 'clickData')],
    [State('country-selector', 'value')]
     )
    def update_country_selection(clickData, current_countries):
    # Si aucun clic n'a été effectué, retournez la sélection actuelle
     if not clickData:
        return current_countries
    
    # Récupérer le nom du pays cliqué
     clicked_country = clickData['points'][0]['location']
    
    # Si aucun pays n'est actuellement sélectionné, créez une nouvelle liste
     if not current_countries:
        return [clicked_country]
    
    # Si le pays est déjà sélectionné, le désélectionnez
     if clicked_country in current_countries:
        return [country for country in current_countries if country != clicked_country]
    
    # Sinon, ajoutez le pays à la sélection
     return current_countries + [clicked_country]
# In your main app file
def register_sidebar_toggle_callback(app):

    @callback(
    Output("menu-sidebar", "style"),  # Output pour changer le style (visibilité)
    Input("menu-button", "n_clicks"),  # Input : clic sur le bouton
    State("menu-sidebar", "style")  # État actuel du style du menu
)
    def toggle_menu(n_clicks, current_style):
     if n_clicks:
        # Toggle the `transform` property
        if current_style['transform'] == 'translateX(0)':
            current_style['transform'] = 'translateX(-100%)'  # Cache le menu
        else:
            current_style['transform'] = 'translateX(0)'  # Affiche le menu
     return current_style
    
    @app.callback(
        [
            Output("filter-collapse", "is_open"),
            Output("filter-toggle-icon", "style"),
        ],
        [Input("filter-toggle-icon", "n_clicks")],
        [State("filter-collapse", "is_open")],
        prevent_initial_call=True
    )
    def toggle_filter_form(n_clicks, is_open):
        if n_clicks is None:
            return True, {'cursor': 'pointer', 'transform': 'rotate(0deg)', 'transition': 'transform 0.3s ease'}
        
        # Toggle the collapse
        new_is_open = not is_open
        
        # Rotate icon based on state
        icon_style = {
            'cursor': 'pointer', 
            'transform': 'rotate(90deg)' if not new_is_open else 'rotate(0deg)',
            'transition': 'transform 0.3s ease'
        }
        
        return new_is_open, icon_style

