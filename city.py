import requests
import tkinter as tk
from tkinter import messagebox, ttk
import ast  # To safely evaluate string representations of Python literals

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
    year = year_combobox.get()  # Get selected year from combobox
    
    if not year:  # Check if a year is selected
        messagebox.showerror("Fout", "Selecteer een jaar.")
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

def load_years_from_file(file_name):
    years = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                # Convert string representation of dictionary to a Python dictionary
                try:
                    data_dict = ast.literal_eval(line.strip())
                    for year in data_dict.keys():
                        years.append(year)  # Add only the year to the list
                except (SyntaxError, ValueError):
                    continue  # Skip lines that cannot be parsed
    except FileNotFoundError:
        messagebox.showerror("Fout", f"Bestand {file_name} niet gevonden.")
    return years

# Set up the Tkinter window
root = tk.Tk()
root.title("Stad Coördinaten Opvragen")

# Create a label and entry for city name input
label_city = tk.Label(root, text="Voer de naam van de stad in:")
label_city.pack(pady=10)

city_entry = tk.Entry(root, width=50)
city_entry.pack(pady=10)

# Create a label for year selection
label_year = tk.Label(root, text="Kies een jaar:")
label_year.pack(pady=10)

# Load years from year.txt and populate the combobox
years = load_years_from_file('year.txt')

year_combobox = ttk.Combobox(root, values=years, state="readonly")
year_combobox.pack(pady=10)
if years:  # Set the default selected year to the first one if available
    year_combobox.current(0)

# Create a button to fetch the coordinates
fetch_button = tk.Button(root, text="Zoek Coördinaten", command=fetch_location)
fetch_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
