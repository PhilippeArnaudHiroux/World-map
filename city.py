import tkinter as tk
from tkinter import messagebox, ttk
import ast  # To safely evaluate string representations of Python literals
from my_functions import get_lat_long_openweathermap, load_years_from_file

def fetch_location():
    city_name = city_entry.get()  # Get the city name entered by the user
    year = year_combobox.get()  # Get selected year from the combobox
    
    if not year:  # Check if a year is selected
        messagebox.showerror("Error", "Select a year.")  # Show an error if no year is selected
        return
    
    api_key = '29c971711cb3db394b7fb7ad51ac44cb'  # Replace with your own API key for OpenWeatherMap
    latitude, longitude = get_lat_long_openweathermap(city_name, api_key)  # Fetch latitude and longitude for the city

    if latitude and longitude:  # If coordinates are found
        result_text = (f"The latitude of {city_name} is: {latitude}\n"  # Prepare result message with latitude
                       f"The longitude of {city_name} is: {longitude}\n"  # Add longitude to result message
                       f"Label: {year}")  # Add selected year as label to result message
        messagebox.showinfo("Result", result_text)  # Show result in an info messagebox 
        text_to_save = f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}'}}"  # Prepare the text for saving to file
        
        with open('location.txt', 'a') as bestand:  # Open 'location.txt' for appending
            bestand.write(text_to_save + '\n')  # Write the prepared text to the file, followed by a newline character
    else:
        messagebox.showerror("Error", f"No data found for {city_name}.")  # Show an error if no location data is found

def show_remove_frame():
    main_frame.pack_forget()  # Hide the main frame
    remove_frame.pack(pady=20)  # Show the remove frame
    update_city_list()

def update_city_list():
    # Clear the current list
    for city in city_listbox.get(0, tk.END):
        city_listbox.delete(0, tk.END)
    
    # Load saved cities
    try:
        with open('location.txt', 'r') as bestand:
            lines = bestand.readlines()
            for line in lines:
                data = ast.literal_eval(line.strip())  # Safely evaluate the string representation
                city_listbox.insert(tk.END, data['name'])  # Insert city names into the listbox
    except FileNotFoundError:
        pass  # If the file doesn't exist, just do nothing


def remove_city():
    selected_city_index = city_listbox.curselection()  # Get the selected city index
    if not selected_city_index:  # If no city is selected
        messagebox.showerror("Error", "Select a city to remove.")  # Show error
        return

    selected_city = city_listbox.get(selected_city_index)  # Get the selected city
    # Read all lines and filter out the selected city
    with open('location.txt', 'r') as bestand:
        lines = bestand.readlines()

    with open('location.txt', 'w') as bestand:  # Open file to write
        for line in lines:
            data = ast.literal_eval(line.strip())
            if data['name'] != selected_city:  # Only write back if the city name doesn't match
                bestand.write(line)  # Write the line back to file

    update_city_list()  # Refresh the city list after removal

# Set up the Tkinter window
root = tk.Tk()
root.title("Request City Coordinates")

# Create main frame for city coordinates
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Create a label and entry for city name input
label_city = tk.Label(main_frame, text="Enter the name of a place:")
label_city.pack(pady=10)

city_entry = tk.Entry(main_frame, width=50)
city_entry.pack(pady=10)

# Create a label for year selection
label_year = tk.Label(main_frame, text="Choose a label:")
label_year.pack(pady=10)

# Load years from year.txt and populate the combobox
years = load_years_from_file('labels.txt')

year_combobox = ttk.Combobox(main_frame, values=years, state="readonly")
year_combobox.pack(pady=10)
if years:  # Set the default selected year to the first one if available
    year_combobox.current(0)

# Create a button to fetch the coordinates
fetch_button = tk.Button(main_frame, text="+", command=fetch_location, fg="green", font=("Arial", 20))
fetch_button.pack(pady=20)

# Create a button to show the remove city frame
remove_button = tk.Button(main_frame, text="Remove City", command=show_remove_frame)
remove_button.pack(pady=5)

# Frame for removing cities
remove_frame = tk.Frame(root)

# Create a label for the remove city section
label_remove = tk.Label(remove_frame, text="Select a city to remove:")
label_remove.pack(pady=10)

# Create a listbox to display saved cities
city_listbox = tk.Listbox(remove_frame, width=50)
city_listbox.pack(pady=10)

# Create a button to remove the selected city
remove_city_button = tk.Button(remove_frame, text="X", command=remove_city, fg="red", font=("Arial", 20))
remove_city_button.pack(pady=10)

# Back button to return to the main frame
back_button = tk.Button(remove_frame, text="Back to Main", command=lambda: [remove_frame.pack_forget(), main_frame.pack(pady=20)])
back_button.pack(pady=10)

# Footer label
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Place the label at the bottom with some space

# Run the Tkinter event loop
root.mainloop()
