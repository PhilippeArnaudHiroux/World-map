import requests
import tkinter as tk
from tkinter import messagebox

def get_lat_long_openweathermap(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data:
        location = data[0]
        return location['lat'], location['lon']
    else:
        return None, None

def fetch_location():
    city_name = city_entry.get()
    year = year_entry.get()
    
    if not year.isdigit() or not (1900 <= int(year) <= 2100):
        messagebox.showerror("Fout", "Voer een geldig jaar in (tussen 1900 en 2100).")
        return
    
    api_key = '29c971711cb3db394b7fb7ad51ac44cb'  # Replace with your own API key
    latitude, longitude = get_lat_long_openweathermap(city_name, api_key)

    if latitude and longitude:
        result_text = (f"De breedtegraad van {city_name} is: {latitude}\n"
                       f"De lengtegraad van {city_name} is: {longitude}\n"
                       f"Jaar: {year}")
        messagebox.showinfo("Resultaat", result_text)

        # Prepare the text for saving
        text_to_save = f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'year': '{year}'}}"
        
        # Open the file in append mode ('a')
        with open('location.txt', 'a') as bestand:
            # Write the text to the file followed by a newline character
            bestand.write(text_to_save + '\n')
    else:
        messagebox.showerror("Fout", f"Geen gegevens gevonden voor {city_name}.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Stad Coördinaten Opvragen")

# Create a label and entry for city name input
label_city = tk.Label(root, text="Voer de naam van de stad in:")
label_city.pack(pady=10)

city_entry = tk.Entry(root, width=50)
city_entry.pack(pady=10)

# Create a label and entry for year input
label_year = tk.Label(root, text="Voer het jaar in (bijv. 2020):")
label_year.pack(pady=10)

year_entry = tk.Entry(root, width=50)
year_entry.pack(pady=10)

# Create a button to fetch the coordinates
fetch_button = tk.Button(root, text="Zoek Coördinaten", command=fetch_location)
fetch_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
