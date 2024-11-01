import plotly.express as px
import pandas as pd
from data import import_data_from_file

cities = import_data_from_file()
print(cities)

# Zet de data om in een DataFrame
df = pd.DataFrame(cities)

# Maak de interactieve kaart
fig = px.scatter_geo(df,
                     lon='lon',
                     lat='lat',
                     hover_name='name',  # De naam van de stad verschijnt bij hover
                     title='My world map!',
                     projection='natural earth',
                     hover_data={'lon': False, 'lat': False}  # Verberg lon en lat bij hover
                     )

# Pas de kleur en grootte van de stippen aan
fig.update_traces(marker=dict(color='red', size=5))  # Rode stippen met grootte 10

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
    showlegend=True,
    plot_bgcolor='black',  # Achtergrondkleur van de plot
    paper_bgcolor='black',  # Achtergrondkleur van de pagina
    font=dict(color='white')  # Kleur van de tekst
)

# Toon de kaart
fig.show()