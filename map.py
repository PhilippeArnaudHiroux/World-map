import plotly.express as px
import pandas as pd

def import_data_from_file(filename):
    data_list = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Verwijder witruimtes aan het begin en einde van de regel
            if line:  # Alleen niet-lege regels verwerken
                try:
                    # Verander de string naar een dictionary door gebruik te maken van eval
                    data = eval(line)  # Gebruik eval() hier
                    if isinstance(data, dict):  # Verifieer dat het een dictionary is
                        data_list.append(data)
                    else:
                        print(f"Regel is geen dictionary: {line}")
                except (SyntaxError, ValueError) as e:
                    print(f"Fout bij het verwerken van regel: {line}. Foutmelding: {e}")
                    
    return data_list

filename = 'location.txt'
cities = import_data_from_file(filename)
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