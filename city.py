import requests

def get_lat_long_openweathermap(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data:
        location = data[0]
        return location['lat'], location['lon']
    else:
        return None, None


city_name = input("Voer de naam van de stad in: ")
api_key = '29c971711cb3db394b7fb7ad51ac44cb'  # Vervang dit met je eigen API-sleutel
latitude, longitude = get_lat_long_openweathermap(city_name, api_key)
if latitude and longitude:
    print(f"De breedtegraad van {city_name} is: {latitude}")
    print(f"De lengtegraad van {city_name} is: {longitude}")
else:
    print(f"Geen gegevens gevonden voor {city_name}.")

tekst = "{'name': '" + city_name  + "', 'lon': " + str(longitude) + ", 'lat': " + str(latitude) + "}"
{'name': 'Amsterdam', 'lon': 4.9041, 'lat': 52.3676}


# Open het bestand in appendmodus ('a')
with open('location.txt', 'a') as bestand:
    # Schrijf de tekst naar het bestand gevolgd door een newline karakter
    bestand.write(tekst + '\n')