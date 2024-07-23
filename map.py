import plotly.express as px
import pandas as pd

# Lijst van steden met coördinaten
cities = [
    {'name': 'Amsterdam', 'lon': 4.9041, 'lat': 52.3676},
    {'name': 'New York', 'lon': -74.0060, 'lat': 40.7128},
    {'name': 'Tokyo', 'lon': 139.6917, 'lat': 35.6895},
    {'name': 'Sydney', 'lon': 151.2093, 'lat': -33.8688},
    {'name': 'Cape Town', 'lon': 18.4241, 'lat': -33.9249},
    {'name': 'Tienen', 'lon': 4.9622, 'lat': 50.8112},
    {'name': 'Leuven', 'lon': 4.7009, 'lat': 50.8790},
    {'name': 'Vertrijk', 'lon': 4.9871, 'lat': 50.8000},
    {'name': 'Carcassonne', 'lon': 2.3537, 'lat': 43.2123}
]

# Zet de data om in een DataFrame
df = pd.DataFrame(cities)

# Maak de interactieve kaart
fig = px.scatter_geo(df,
                     lon='lon',
                     lat='lat',
                     hover_name='name',  # De naam van de stad verschijnt bij hover
                     title='Wereldkaart met Steden en Landgrenzen',
                     projection='natural earth',
                     hover_data={'lon': False, 'lat': False}  # Verberg lon en lat bij hover
                     )

# Pas de kleur en grootte van de stippen aan
fig.update_traces(marker=dict(color='red', size=10))  # Rode stippen met grootte 10

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
    countrycolor='black'
)

# Pas de layout aan voor beter zicht
fig.update_layout(
    title='Wereldkaart met Interactieve Steden en Landgrenzen',
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
    showlegend=False
)

# Toon de kaart
fig.show()
