import tkinter as tk
from tkinter import messagebox
import subprocess  # Om een ander Python-script aan te roepen

def open_city_window():
    # Start het script voor het toevoegen van een stad
    subprocess.Popen(['python', 'city.py'])

def open_year_window():
    # Start het script voor het toevoegen van een jaar
    subprocess.Popen(['python', 'year.py'])

def open_map_window():
    # Start het script voor het toevoegen van een jaar
    subprocess.Popen(['python', 'map.py'])

# Hoofdvenster instellen
root = tk.Tk()
root.title("Hoofdmenu")

# Creëer knoppen voor stad toevoegen en jaar toevoegen
add_city_button = tk.Button(root, text="Stad Toevoegen", command=open_city_window, width=30)
add_city_button.pack(pady=20)

add_year_button = tk.Button(root, text="Jaar Toevoegen", command=open_year_window, width=30)
add_year_button.pack(pady=20)

add_year_button = tk.Button(root, text="Map tonen", command=open_map_window, width=30)
add_year_button.pack(pady=20)

# Start de Tkinter event loop
root.mainloop()
