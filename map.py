import plotly.express as px
import pandas as pd
from my_functions import import_data_from_file, import_year_from_file

# Importeer de data
cities = import_data_from_file()         # Informatie over de steden
year_data = import_year_from_file()      # Informatie over de kleuren per jaar

# Zet de data om in een DataFrame
df = pd.DataFrame(cities)

# Maak een kleur-mapping van jaar naar kleur
year_color_map = {}
for year_dict in year_data:
    for year, color in year_dict.items():
        # Converteer de hexadecimale string naar een integer, dan naar een hexadecimale string in #RRGGBB-formaat
        color_int = int(color, 16)  # Zet de hex-string om naar een integer
        hex_color = "#{:06X}".format(color_int)  # Converteer integer naar hexadecimale string in #RRGGBB-formaat
        year_color_map[year] = hex_color


# Controleer of de mapping correct is
print("Year to Color Mapping:", year_color_map)

# Voeg een kleur toe aan de DataFrame op basis van het jaar
df['color'] = df['label'].map(year_color_map)

# Controleer of de kleuren correct zijn toegewezen aan de DataFrame
print("DataFrame with colors:", df)

# Maak de interactieve kaart
fig = px.scatter_geo(df,
                    lon='lon',
                    lat='lat',
                    hover_name='name',  # De naam van de stad verschijnt bij hover
                    title='My world map!',
                    projection='natural earth',
                    color='label',  # Gebruik het jaar voor kleuren
                    color_discrete_map=year_color_map,  # Koppel kleuren aan jaren
                    hover_data={'lon': False, 'lat': False, 'label': False}  # Verberg lon, lat en year bij hover
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
    legend_title_text='Labels',  # Titel van de legende
    plot_bgcolor='black',  # Achtergrondkleur van de plot
    paper_bgcolor='black',  # Achtergrondkleur van de pagina
    font=dict(color='white')  # Kleur van de tekst
)

# Sla de kaart op als HTML-bestand
fig.write_html("world_map.html")

# Toon de kaart
fig.show()