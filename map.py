import plotly.express as px
import pandas as pd
from data import import_data_from_file, import_year_from_file

# Importeer de data
cities = import_data_from_file()         # Informatie over de steden
year_data = import_year_from_file()      # Informatie over de kleuren per jaar

# Zet de data om in een DataFrame
df = pd.DataFrame(cities)

# Maak een kleur-mapping van jaar naar kleur
year_color_map = {}
for year_dict in year_data:
    for year, color in year_dict.items():
        # Omzetten naar hex formaat
        year_color_map[year] = "#{:06X}".format(color)

# Controleer of de mapping correct is
print("Year to Color Mapping:", year_color_map)

# Voeg een kleur toe aan de DataFrame op basis van het jaar
df['color'] = df['year'].map(year_color_map)

# Controleer of de kleuren correct zijn toegewezen aan de DataFrame
print("DataFrame with colors:", df)

# Create a new DataFrame for legend with unique years and colors
legend_df = pd.DataFrame(year_color_map.items(), columns=['year', 'color'])

# Maak de interactieve kaart
fig = px.scatter_geo(df,
                     lon='lon',
                     lat='lat',
                     hover_name='name',  # De naam van de stad verschijnt bij hover
                     title='My world map!',
                     projection='natural earth',
                     color='year',  # Use the year for colors
                     color_discrete_map=year_color_map,  # Map colors to years
                     hover_data={'lon': False, 'lat': False}  # Verberg lon en lat bij hover
                     )

# Pas de grootte van de stippen aan
fig.update_traces(marker=dict(size=10))  # Pas de grootte naar wens aan

# Voeg landgrenzen toe
fig.update_geos(
    showland=True,
    landcolor='lightgreen',
    showocean=True,
    oceancolor='lightblue',
    showcoastlines=True,
    coastlinecolor='black',
    showlakes=True,
    lakecolor='lightblue',
    showrivers=True,
    rivercolor='blue',
    showcountries=True,  # Deze regel zorgt voor de landgrenzen
    countrycolor='black',
    showframe=False,  # Verberg frame rond de kaart
    resolution=50,  # Hogere resolutie voor meer details
    projection_scale=1,  # Schaal van de projectie
    bgcolor='black'  # Achtergrondkleur van de kaart
)

# Pas de layout aan voor beter zicht
fig.update_layout(
    title='My world map!',
    geo=dict(
        showland=True,
        landcolor='lightgreen',
        oceancolor='lightblue',
        showocean=True,
        showcoastlines=True,
        coastlinecolor='black',
        showlakes=True,
        lakecolor='lightblue',
        showrivers=True,
        rivercolor='blue',
        showcountries=True,
        countrycolor='black'
    ),
    showlegend=True,  # Zorg ervoor dat de legende wordt getoond
    legend_title_text='Year',  # Titel van de legende
    plot_bgcolor='black',  # Achtergrondkleur van de plot
    paper_bgcolor='black',  # Achtergrondkleur van de pagina
    font=dict(color='white')  # Kleur van de tekst
)

# Sla de kaart op als HTML-bestand
fig.write_html("world_map.html")

# Toon de kaart
fig.show()
