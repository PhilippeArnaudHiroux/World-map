import tkinter as tk
from tkinter import messagebox, ttk
import ast  # Voor veilig evalueren van stringrepresentaties van Python-literals
import pycountry
from my_functions import get_lat_long_openweathermap, load_labels_from_file

# Functie om locatiegegevens op te halen
def fetch_location():
    city_name = city_entry.get().capitalize()
    year = year_combobox.get()

    if not year:
        messagebox.showerror("Error", "Select a label.")
        return

    api_key = '29c971711cb3db394b7fb7ad51ac44cb'
    latitude, longitude, country = get_lat_long_openweathermap(city_name, api_key)

    if latitude and longitude:
        result_text = (f"The latitude of {city_name} is: {latitude}\n"
                       f"The longitude of {city_name} is: {longitude}\n"
                       f"The country of {city_name} is: {country}\n"
                       f"Label: {year}")
        messagebox.showinfo("Result", result_text)
        text_to_save = f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}', 'country': '{country}'}}"
        
        with open('location.txt', 'a') as bestand:
            bestand.write(text_to_save + '\n')
    else:
        messagebox.showerror("Error", f"No data found for {city_name}.")

# Functie om het handmatige invoerscherm te openen
def open_manual_add_screen():
    main_frame.pack_forget()
    manual_frame.pack(pady=20)

def save_manual_entry():
    city_name = entry_city.get().capitalize()
    latitude = entry_latitude.get()
    longitude = entry_longitude.get()
    country_code = entry_country.get().upper()
    label = label_combobox.get()
    
    if not city_name or not latitude or not longitude or not country_code or not label:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        country_name = pycountry.countries.get(alpha_2=country_code).name if pycountry.countries.get(alpha_2=country_code) else "Unknown country"
        text_to_save = (f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, "
                        f"'label': '{label}', 'country': '{country_name}'}}")
        with open('location.txt', 'a') as bestand:
            bestand.write(text_to_save + '\n')
        messagebox.showinfo("Success", f"{city_name} has been added manually.")
        load_main_screen()
    except ValueError:
        messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.")

# Functie om het verwijderformulier te tonen
def show_remove_frame():
    main_frame.pack_forget()
    remove_frame.pack(pady=20)
    update_country_list()
    country_combobox.current(0)
    update_label_list()
    label_combobox.current(0)
    update_city_list()

# Functies om de keuzelijsten te updaten
def update_country_list():
    country_combobox['values'] = []
    countries = set()
    try:
        with open('location.txt', 'r') as bestand:
            lines = bestand.readlines()
            for line in lines:
                data = ast.literal_eval(line.strip())
                countries.add(data['country'])
        country_combobox['values'] = ["All places"] + sorted(list(countries))
        update_city_list()
    except FileNotFoundError:
        pass

def update_label_list():
    label_combobox['values'] = []
    try:
        with open('labels.txt', 'r') as bestand:
            labels = [list(ast.literal_eval(line.strip()).keys())[0] for line in bestand]
        label_combobox['values'] = ["All labels"] + sorted(labels)
        label_combobox.current(0)
    except FileNotFoundError:
        pass

def update_city_list(event=None):
    city_listbox.delete(0, tk.END)
    selected_country = country_combobox.get()
    selected_label = label_combobox.get()
    try:
        with open('location.txt', 'r') as bestand:
            for line in bestand:
                data = ast.literal_eval(line.strip())
                if (selected_country == "All places" or data['country'] == selected_country) and \
                   (selected_label == "All labels" or data['label'] == selected_label):
                    city_listbox.insert(tk.END, data['name'])
    except FileNotFoundError:
        pass

# Functie om geselecteerde stad te verwijderen
def remove_city():
    selected_city_index = city_listbox.curselection()
    if not selected_city_index:
        messagebox.showerror("Error", "Select a place to delete.")
        return

    selected_city = city_listbox.get(selected_city_index)
    with open('location.txt', 'r') as bestand:
        lines = bestand.readlines()

    with open('location.txt', 'w') as bestand:
        for line in lines:
            if ast.literal_eval(line.strip())['name'] != selected_city:
                bestand.write(line)
    update_city_list()

# Functie om terug te keren naar het hoofdscherm
def load_main_screen():
    manual_frame.pack_forget()
    remove_frame.pack_forget()
    main_frame.pack(pady=20)

# Instellen van het Tkinter-venster
root = tk.Tk()
root.title("Request Cities Coordinates")

# Hoofdframe voor stadcoördinaten
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

label_city = tk.Label(main_frame, text="Enter the name of a place:")
label_city.pack(pady=10)
city_entry = tk.Entry(main_frame, width=50)
city_entry.pack(pady=10)

label_year = tk.Label(main_frame, text="Choose a label:")
label_year.pack(pady=10)
labels = load_labels_from_file('labels.txt')
year_combobox = ttk.Combobox(main_frame, values=labels, state="readonly")
year_combobox.pack(pady=10)
if labels:
    year_combobox.current(0)

fetch_button = tk.Button(main_frame, text="+", command=fetch_location, fg="green", font=("Arial", 20))
fetch_button.pack(pady=20)

manual_button = tk.Button(main_frame, text="Add Place Manually", command=open_manual_add_screen)
manual_button.pack(pady=5)
remove_button = tk.Button(main_frame, text="Delete place", command=show_remove_frame)
remove_button.pack(pady=5)

# Frame voor handmatige invoer
manual_frame = tk.Frame(root)
tk.Label(manual_frame, text="Manual Place Entry", font=("Arial", 14)).pack(pady=10)

# Frame voor de invoervelden en hun labels
input_frame = tk.Frame(manual_frame)
input_frame.pack(pady=10)

# Labels en invoervelden naast elkaar plaatsen
tk.Label(input_frame, text="Place Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_city = tk.Entry(input_frame, width=40)
entry_city.grid(row=0, column=1, pady=5)

tk.Label(input_frame, text="Latitude:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_latitude = tk.Entry(input_frame, width=40)
entry_latitude.grid(row=1, column=1, pady=5)

tk.Label(input_frame, text="Longitude:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_longitude = tk.Entry(input_frame, width=40)
entry_longitude.grid(row=2, column=1, pady=5)

tk.Label(input_frame, text="Country Code:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_country = tk.Entry(input_frame, width=40)
entry_country.grid(row=3, column=1, pady=5)

tk.Label(input_frame, text="Label:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
label_combobox = ttk.Combobox(input_frame, values=labels, state="readonly", width=37)
label_combobox.grid(row=4, column=1, pady=5)

# Opslaan knop en terug knop
tk.Button(manual_frame, text="+", command=save_manual_entry, fg="green", font=("Arial", 20)).pack(pady=20)
tk.Button(manual_frame, text="Back", command=load_main_screen).pack(pady=10)


# Frame voor verwijderen
remove_frame = tk.Frame(root)
tk.Label(remove_frame, text="Select a country and city to delete:").pack(pady=10)
combo_frame = tk.Frame(remove_frame)
combo_frame.pack(pady=10)
country_combobox = ttk.Combobox(combo_frame, state="readonly")
country_combobox.pack(side=tk.LEFT, padx=(0, 10))
country_combobox.bind("<<ComboboxSelected>>", lambda event: [update_label_list(), update_city_list()])
label_combobox = ttk.Combobox(combo_frame, state="readonly")
label_combobox.pack(side=tk.LEFT)
label_combobox.bind("<<ComboboxSelected>>", update_city_list)
city_listbox = tk.Listbox(remove_frame, width=50)
city_listbox.pack(pady=10)
remove_city_button = tk.Button(remove_frame, text="X", command=remove_city, fg="red", font=("Arial", 20))
remove_city_button.pack(pady=10)
tk.Button(remove_frame, text="Back", command=load_main_screen).pack(pady=10)

footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Voer de Tkinter-evenloop uit
root.mainloop()
