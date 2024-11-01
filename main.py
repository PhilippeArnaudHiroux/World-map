import tkinter as tk
from tkinter import messagebox
import subprocess  # Om een ander Python-script aan te roepen
from PIL import Image, ImageTk  # Voor het werken met JPG-afbeeldingen

def open_city_window():
    # Start het script voor het toevoegen van een stad
    subprocess.Popen(['python', 'city.py'])

def open_year_window():
    # Start het script voor het toevoegen van een jaar
    subprocess.Popen(['python', 'year.py'])

def open_map_window():
    # Start het script voor het tonen van een map
    subprocess.Popen(['python', 'map.py'])

# Hoofdvenster instellen
root = tk.Tk()
root.title("Hoofdmenu")

# Schaal de afbeeldingen
city_image = ImageTk.PhotoImage(Image.open("image/city.jpg").resize((100, 100)))
year_image = ImageTk.PhotoImage(Image.open("image/Year.jpg").resize((100, 100)))
map_image = ImageTk.PhotoImage(Image.open("image/Map.jpg").resize((100, 100)))

# Maak een frame voor de knoppen
button_frame = tk.Frame(root)
button_frame.pack(pady=20)  # Voeg wat ruimte boven het frame

# Creëer knoppen met afbeeldingen en plaats ze in het frame
add_city_button = tk.Button(button_frame, image=city_image, command=open_city_window)
add_city_button.grid(row=0, column=0, padx=10)  # Voeg wat ruimte tussen de knoppen

add_year_button = tk.Button(button_frame, image=year_image, command=open_year_window)
add_year_button.grid(row=0, column=1, padx=10)  # Voeg wat ruimte tussen de knoppen

add_map_button = tk.Button(button_frame, image=map_image, command=open_map_window)
add_map_button.grid(row=0, column=2, padx=10)  # Voeg wat ruimte tussen de knoppen

# Voeg een label toe onder de knoppen
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Plaats het label onderaan met wat ruimte

# Start de Tkinter event loop
root.mainloop()
