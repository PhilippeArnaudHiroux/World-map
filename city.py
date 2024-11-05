import tkinter as tk
from tkinter import messagebox, ttk
import ast  # Voor veilig evalueren van stringrepresentaties van Python-literals
from my_functions import get_lat_long_openweathermap, load_years_from_file

def fetch_location():
    city_name = city_entry.get()  # Verkrijg de stadsnaam die door de gebruiker is ingevoerd
    year = year_combobox.get()  # Verkrijg het geselecteerde jaar uit de combobox
    
    if not year:  # Controleer of er een jaar is geselecteerd
        messagebox.showerror("Error", "Selecteer een jaar.")  # Toon een foutmelding als er geen jaar is geselecteerd
        return
    
    api_key = '29c971711cb3db394b7fb7ad51ac44cb'  # Vervang door je eigen API-sleutel voor OpenWeatherMap
    latitude, longitude, country = get_lat_long_openweathermap(city_name, api_key)  # Verkrijg breedte- en lengtegraad voor de stad

    if latitude and longitude:  # Als coördinaten zijn gevonden
        result_text = (f"De breedtegraad van {city_name} is: {latitude}\n"  # Bereid resultaatbericht voor met breedtegraad
                       f"De lengtegraad van {city_name} is: {longitude}\n"  # Voeg lengtegraad toe aan resultaatbericht
                       f"Het land van {city_name} is: {country}\n"  # Voeg land toe aan resultaatbericht
                       f"Label: {year}")  # Voeg geselecteerd jaar als label toe aan resultaatbericht
        messagebox.showinfo("Resultaat", result_text)  # Toon resultaat in een info-bericht
        text_to_save = f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}', 'country': '{country}'}}"  # Bereid de tekst voor opslaan in bestand
        
        with open('location.txt', 'a') as bestand:  # Open 'location.txt' voor toevoegen
            bestand.write(text_to_save + '\n')  # Schrijf de voorbereide tekst naar het bestand, gevolgd door een nieuwe regel
    else:
        messagebox.showerror("Error", f"Geen gegevens gevonden voor {city_name}.")  # Toon een foutmelding als er geen locatiegegevens zijn gevonden

def show_remove_frame():
    main_frame.pack_forget()  # Verberg het hoofdscherm
    remove_frame.pack(pady=20)  # Toon het verwijderformulier
    update_country_list()  # Update de lijst van landen
    country_combobox.current(0)  # Zet de standaard selectie naar "Alle Steden"
    update_city_list("Alle steden")  # Update de stadlijst direct bij het openen


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
                    print(f"Fout bij het parseren van regel: {line.strip()} - {e}")  # Print foutmelding

        country_list = ["Alle steden"] + sorted(list(countries))  # Voeg optie toe om alle steden te tonen
        country_combobox['values'] = list(country_list)  # Zet de landen in de combobox
        update_city_list()  # Update de stadlijst direct bij het openen
    except FileNotFoundError:
        pass  # Als het bestand niet bestaat, doe dan niets

def update_city_list(event=None):
    # Leeg de huidige lijst
    city_listbox.delete(0, tk.END)

    selected_country = country_combobox.get()  # Verkrijg het geselecteerde land
    try:
        with open('location.txt', 'r') as bestand:
            lines = bestand.readlines()
            for line in lines:
                data = ast.literal_eval(line.strip())  # Veilig evalueren van de stringrepresentatie
                # Controleer of 'Alle Steden' is geselecteerd of het land overeenkomt
                if selected_country == "Alle steden" or data['country'] == selected_country:
                    city_listbox.insert(tk.END, data['name'])  # Voeg stad toe aan de listbox
    except FileNotFoundError:
        pass  # Als het bestand niet bestaat, doe dan niets



def remove_city():
    selected_city_index = city_listbox.curselection()  # Verkrijg de geselecteerde stad
    if not selected_city_index:  # Als er geen stad is geselecteerd
        messagebox.showerror("Error", "Selecteer een stad om te verwijderen.")  # Toon foutmelding
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
root.title("Vraag Coördinaten van Steden aan")

# Hoofdframe voor stadcoördinaten
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Label en invoer voor stadnaam
label_city = tk.Label(main_frame, text="Voer de naam van een plaats in:")
label_city.pack(pady=10)

city_entry = tk.Entry(main_frame, width=50)
city_entry.pack(pady=10)

# Label voor jaarselectie
label_year = tk.Label(main_frame, text="Kies een label:")
label_year.pack(pady=10)

# Jaren laden vanuit labels.txt en combobox invullen
years = load_years_from_file('labels.txt')

year_combobox = ttk.Combobox(main_frame, values=years, state="readonly")
year_combobox.pack(pady=10)
if years:  # Zet het standaard geselecteerde jaar op het eerste als het beschikbaar is
    year_combobox.current(0)

# Knop om coördinaten op te halen
fetch_button = tk.Button(main_frame, text="+", command=fetch_location, fg="green", font=("Arial", 20))
fetch_button.pack(pady=20)

# Knop om het verwijderformulier te tonen
remove_button = tk.Button(main_frame, text="Verwijder Stad", command=show_remove_frame)
remove_button.pack(pady=5)

# Frame voor het verwijderen van steden
remove_frame = tk.Frame(root)

# Label voor het verwijderen van stadsectie
label_remove = tk.Label(remove_frame, text="Selecteer een land en een stad om te verwijderen:")
label_remove.pack(pady=10)

# Combobox voor het selecteren van landen
country_combobox = ttk.Combobox(remove_frame, state="readonly")
country_combobox.pack(pady=10)
country_combobox.bind("<<ComboboxSelected>>", update_city_list)  # Bind de selectie aan de functie

# Listbox om opgeslagen steden weer te geven
city_listbox = tk.Listbox(remove_frame, width=50)
city_listbox.pack(pady=10)

# Knop om de geselecteerde stad te verwijderen
remove_city_button = tk.Button(remove_frame, text="X", command=remove_city, fg="red", font=("Arial", 20))
remove_city_button.pack(pady=10)

# Terugknop om terug te keren naar het hoofdframe
back_button = tk.Button(remove_frame, text="Terug naar Hoofd", command=lambda: [remove_frame.pack_forget(), main_frame.pack(pady=20)])
back_button.pack(pady=10)

# Voettekst
footer_label = tk.Label(root, text="Gemaakt door Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Plaats het label onderaan met wat ruimte

# Voer de Tkinter-evenloop uit
root.mainloop()
