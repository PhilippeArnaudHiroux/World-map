import tkinter as tk
from tkinter import messagebox, ttk
import ast  # Voor veilig evalueren van stringrepresentaties van Python-literals
from my_functions import get_lat_long_openweathermap, load_years_from_file

def fetch_location():
    city_name = city_entry.get().capitalize()  # Verkrijg de stadsnaam die door de gebruiker is ingevoerd
    year = year_combobox.get()  # Verkrijg het geselecteerde jaar uit de combobox
    
    if not year:  # Controleer of er een jaar is geselecteerd
        messagebox.showerror("Error", "Select a label.")  # Toon een foutmelding als er geen jaar is geselecteerd
        return
    
    api_key = '29c971711cb3db394b7fb7ad51ac44cb'  # Vervang door je eigen API-sleutel voor OpenWeatherMap
    latitude, longitude, country = get_lat_long_openweathermap(city_name, api_key)  # Verkrijg breedte- en lengtegraad voor de stad

    if latitude and longitude:  # Als coördinaten zijn gevonden
        result_text = (f"The latitude of {city_name} is: {latitude}\n"  # Bereid resultaatbericht voor met breedtegraad
                       f"The longitude of {city_name} is: {longitude}\n"  # Voeg lengtegraad toe aan resultaatbericht
                       f"The country of {city_name} is: {country}\n"  # Voeg land toe aan resultaatbericht
                       f"Label: {year}")  # Voeg geselecteerd jaar als label toe aan resultaatbericht
        messagebox.showinfo("Result", result_text)  # Toon resultaat in een info-bericht
        text_to_save = f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}', 'country': '{country}'}}"  # Bereid de tekst voor opslaan in bestand
        
        with open('location.txt', 'a') as bestand:  # Open 'location.txt' voor toevoegen
            bestand.write(text_to_save + '\n')  # Schrijf de voorbereide tekst naar het bestand, gevolgd door een nieuwe regel
    else:
        messagebox.showerror("Error", f"No data found for {city_name}.")  # Toon een foutmelding als er geen locatiegegevens zijn gevonden

def show_remove_frame():
    main_frame.pack_forget()  # Verberg het hoofdscherm
    remove_frame.pack(pady=20)  # Toon het verwijderformulier
    update_country_list()  # Update de lijst van landen
    country_combobox.current(0)  # Zet de standaard selectie naar "Alle Steden"
    update_label_list()  # Update de label lijst bij het openen
    label_combobox.current(0)  # Zet de standaard selectie naar "Alle Labels"
    update_city_list()  # Update de stadlijst direct bij het openen

def update_country_list():
    country_combobox['values'] = []
    countries = set()  # Gebruik een set om duplicaten te vermijden

    try:
        with open('location.txt', 'r') as bestand:
            lines = bestand.readlines()
            for line in lines:
                try:
                    data = ast.literal_eval(line.strip())  # Veilig evalueren van de stringrepresentatie
                    countries.add(data['country'])  # Voeg land toe aan de set
                except SyntaxError as e:
                    print(f"Error parsing line: {line.strip()} - {e}")  # Print foutmelding

        country_list = ["All places"] + sorted(list(countries))  # Voeg optie toe om alle steden te tonen
        country_combobox['values'] = list(country_list)  # Zet de landen in de combobox
        update_city_list()  # Update de stadlijst direct bij het openen
    except FileNotFoundError:
        pass  # Als het bestand niet bestaat, doe dan niets

def update_label_list():
    label_combobox['values'] = []  # Reset de label lijst
    try:
        with open('labels.txt', 'r') as bestand:
            lines = bestand.readlines()
            labels = []  # Lijst om de labels op te slaan
            for line in lines:
                try:
                    data = ast.literal_eval(line.strip())  # Veilig evalueren van de stringrepresentatie
                    labels.append(list(data.keys())[0])  # Neem de label naam (de eerste sleutel)
                except SyntaxError as e:
                    print(f"Error parsing line: {line.strip()} - {e}")  # Print foutmelding

            label_combobox['values'] = ["All labels"] + sorted(labels)  # Voeg optie toe voor alle labels
            label_combobox.current(0)  # Zet de standaard selectie naar "Alle Labels"
    except FileNotFoundError:
        pass  # Als het bestand niet bestaat, doe dan niets

def update_city_list(event=None):
    # Leeg de huidige lijst
    city_listbox.delete(0, tk.END)

    selected_country = country_combobox.get()  # Verkrijg het geselecteerde land
    selected_label = label_combobox.get()  # Verkrijg het geselecteerde label

    try:
        with open('location.txt', 'r') as bestand:
            lines = bestand.readlines()
            for line in lines:
                data = ast.literal_eval(line.strip())  # Veilig evalueren van de stringrepresentatie
                # Controleer of 'Alle Steden' is geselecteerd of het land overeenkomt
                if (selected_country == "All places" or data['country'] == selected_country) and \
                        (selected_label == "All labels" or data['label'] == selected_label):
                    city_listbox.insert(tk.END, data['name'])  # Voeg stad toe aan de listbox
    except FileNotFoundError:
        pass  # Als het bestand niet bestaat, doe dan niets

def remove_city():
    selected_city_index = city_listbox.curselection()  # Verkrijg de geselecteerde stad
    if not selected_city_index:  # Als er geen stad is geselecteerd
        messagebox.showerror("Error", "Select a place to delete.")  # Toon foutmelding
        return

    selected_city = city_listbox.get(selected_city_index)  # Verkrijg de geselecteerde stad
    # Lees alle regels en filter de geselecteerde stad eruit
    with open('location.txt', 'r') as bestand:
        lines = bestand.readlines()

    with open('location.txt', 'w') as bestand:  # Open bestand om te schrijven
        for line in lines:
            data = ast.literal_eval(line.strip())
            if data['name'] != selected_city:  # Alleen schrijven als de stad niet overeenkomt
                bestand.write(line)  # Schrijf de regel terug naar het bestand

    update_city_list()  # Vernieuw de lijst van steden na verwijdering

# Instellen van het Tkinter-venster
root = tk.Tk()
root.title("Request Cities Coordinates")

# Hoofdframe voor stadcoördinaten
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Label en invoer voor stadnaam
label_city = tk.Label(main_frame, text="Enter the name of a place:")
label_city.pack(pady=10)

city_entry = tk.Entry(main_frame, width=50)
city_entry.pack(pady=10)

# Label voor jaarselectie
label_year = tk.Label(main_frame, text="Choose a label:")
label_year.pack(pady=10)

# Jaren laden vanuit labels.txt en combobox invullen
labels = load_years_from_file('labels.txt')

year_combobox = ttk.Combobox(main_frame, values=labels, state="readonly")
year_combobox.pack(pady=10)
if labels:  # Zet het standaard geselecteerde jaar op het eerste als het beschikbaar is
    year_combobox.current(0)

# Knop om coördinaten op te halen
fetch_button = tk.Button(main_frame, text="+", command=fetch_location, fg="green", font=("Arial", 20))
fetch_button.pack(pady=20)

# Knop om het verwijderformulier te tonen
remove_button = tk.Button(main_frame, text="Delete place", command=show_remove_frame)
remove_button.pack(pady=5)

# Frame voor het verwijderen van steden
remove_frame = tk.Frame(root)

# Label voor het verwijderen van stadsectie
label_remove = tk.Label(remove_frame, text="Select a country and city to delete:")
label_remove.pack(pady=10)

# Frame voor de comboboxen voor landen en labels
combo_frame = tk.Frame(remove_frame)
combo_frame.pack(pady=10)  # Voeg padding toe aan het frame

# Combobox voor het selecteren van landen
country_combobox = ttk.Combobox(combo_frame, state="readonly")
country_combobox.pack(side=tk.LEFT, padx=(0, 10))  # Plaats links in het combo_frame
country_combobox.bind("<<ComboboxSelected>>", lambda event: [update_label_list(), update_city_list(event)])  # Bind de selectie aan de functie

# Toevoegen van een combobox voor labels
label_combobox = ttk.Combobox(combo_frame, state="readonly")
label_combobox.pack(side=tk.LEFT)  # Plaats rechts in het combo_frame
label_combobox.bind("<<ComboboxSelected>>", update_city_list)  # Bind de label selectie aan de functie

# Listbox om opgeslagen steden weer te geven
city_listbox = tk.Listbox(remove_frame, width=50)
city_listbox.pack(pady=10)

# Knop om de geselecteerde stad te verwijderen
remove_city_button = tk.Button(remove_frame, text="X", command=remove_city, fg="red", font=("Arial", 20))
remove_city_button.pack(pady=10)

# Terugknop om terug te keren naar het hoofdframe
back_button = tk.Button(remove_frame, text="Back", command=lambda: [remove_frame.pack_forget(), main_frame.pack(pady=20)])
back_button.pack(pady=10)

# Voettekst
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Plaats het label onderaan met wat ruimte

# Voer de Tkinter-evenloop uit
root.mainloop()
