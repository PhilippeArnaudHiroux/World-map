import plotly.express as px
import pandas as pd
from data import import_data_from_file

# Importeer de data
cities = import_data_from_file()
print(cities)

# Zet de data om in een DataFrame
df = pd.DataFrame(cities)

# Zorg ervoor dat RGB-waarden in hex-formaat zijn
# Zet de RGB-waarden om naar hex
df['color'] = df['rgb'].apply(lambda x: "#{:06X}".format(x))

# Maak de interactieve kaart
fig = px.scatter_geo(df,
                     lon='lon',
                     lat='lat',
                     hover_name='name',  # De naam van de stad verschijnt bij hover
                     title='My world map!',
                     projection='natural earth',
                     color='name',  # Gebruik de naam als kleur categorisch
                     color_discrete_map={row['name']: row['color'] for _, row in df.iterrows()},  # Specificeer de kleuren voor elke naam
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
    legend_title_text='Cities',  # Titel van de legende
    plot_bgcolor='black',  # Achtergrondkleur van de plot
    paper_bgcolor='black',  # Achtergrondkleur van de pagina
    font=dict(color='white')  # Kleur van de tekst
)

# Sla de kaart op als HTML-bestand
fig.write_html("world_map.html")

# Toon de kaart
fig.show()
