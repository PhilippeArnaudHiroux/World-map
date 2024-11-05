import tkinter as tk
from tkinter import messagebox, ttk
import ast  # To safely evaluate string representations of Python literals
from my_functions import get_lat_long_openweathermap, load_years_from_file

def fetch_location(city_entry, year_combobox):
    city_name = city_entry.get()                                                                                #Get the city name entered by the user
    year = year_combobox.get()                                                                                  #Get selected year from the combobox
    
    if not year:                                                                                                #Check if a year is selected
        messagebox.showerror("Error", "Select a year.")                                                         #Show an error if no year is selected
        return
    
    api_key = '29c971711cb3db394b7fb7ad51ac44cb'                                                                #Replace with your own API key for OpenWeatherMap
    latitude, longitude = get_lat_long_openweathermap(city_name, api_key)                                       #Fetch latitude and longitude for the city

    if latitude and longitude:                                                                                  #If coordinates are found
        result_text = (f"The latitude of {city_name} is: {latitude}\n"                                          #Prepare result message with latitude
                       f"The longitude of {city_name} is: {longitude}\n"                                        #Add longitude to result message
                       f"Label: {year}")                                                                        #Add selected year as label to result message
        messagebox.showinfo("Result", result_text)                                                              #Show result in an info messagebox 
        text_to_save = f"\n{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}'}}" #Prepare the text for saving to file
        
        with open('location.txt', 'a') as bestand:                                                              #Open 'location.txt' for appending
            bestand.write(text_to_save + '\n')                                                                  #Write the prepared text to the file, followed by a newline character
    else:
        messagebox.showerror("Error", f"No data found for {city_name}.")                                        #Show an error if no location data is found

# Set up the Tkinter window
root = tk.Tk()
root.title("Request City Coordinates")

# Create a label and entry for city name input
label_city = tk.Label(root, text="Enter the name of a place:")
label_city.pack(pady=10)

city_entry = tk.Entry(root, width=50)
city_entry.pack(pady=10)

# Create a label for year selection
label_year = tk.Label(root, text="Choose a label:")
label_year.pack(pady=10)

# Load years from year.txt and populate the combobox
years = load_years_from_file('labels.txt')

year_combobox = ttk.Combobox(root, values=years, state="readonly")
year_combobox.pack(pady=10)
if years:  # Set the default selected year to the first one if available
    year_combobox.current(0)

# Create a button to fetch the coordinates
fetch_button = tk.Button(root, text="Search Coordinates", command=fetch_location)
fetch_button.pack(pady=20)

# Voeg een label toe onder de knoppen
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Plaats het label onderaan met wat ruimte

# Run the Tkinter event loop
root.mainloop()
