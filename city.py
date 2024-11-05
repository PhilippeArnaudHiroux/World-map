import tkinter as tk                                                        #Import the tkinter library for creating the GUI
from tkinter import messagebox, ttk                                         #Import specific modules from tkinter for message boxes and themed widgets
import ast                                                                  #Import ast module for safely evaluating string representations of Python literals
import pycountry                                                            #Import pycountry to work with country information and codes
from my_functions import get_lat_long_openweathermap, load_labels_from_file #Import custom functions for fetching location data and loading labels from a file



def fetch_location():################################################################################################################Function to fetch location data
    city_name=city_entry.get().capitalize()                                                                                         #Get the city name from the entry field and capitalize it
    year=year_combobox.get()                                                                                                        #Get the selected label (year) from the combobox
    if not year:                                                                                                                    #If there is no label
        messagebox.showerror("Error", "Select a label.")                                                                            #Show error if no label (year) is selected
        return                                                                                                                      #Go out the function
    latitude, longitude, country=get_lat_long_openweathermap(city_name)                                                             #Fetch latitude, longitude, and country using API
    if latitude and longitude:                                                                                                      #If there is a latitude and longitude found
        result_text=(f"The latitude of {city_name} is: {latitude}\n"                                                                #Format result text with location details
                     f"The longitude of {city_name} is: {longitude}\n"                                                              #Format result text with location details
                     f"The country of {city_name} is: {country}\n"                                                                  #Format result text with location details
                     f"Label: {year}")                                                                                              #Format result text with location details
        messagebox.showinfo("Result", result_text)                                                                                  #Show the result text in an information box
        text_to_save=f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, 'label': '{year}', 'country': '{country}'}}" #Format text to save location data in JSON-like structure
        with open('location.txt', 'a') as bestand:                                                                                  #Open file in append mode to add new data
            bestand.write(text_to_save + '\n')                                                                                      #Write location data to the file with a newline
    else:                                                                                                                           #If there is no latitude and longitude found
        messagebox.showerror("Error", f"No data found for {city_name}.")                                                            #Show error if location data is not found

def open_manual_add_screen():####Function to open the manual input screen
    main_frame.pack_forget()    #Hide the main frame
    manual_frame.pack(pady=20)  #Display the manual input frame with padding of 20 pixels at the top

def save_manual_entry():#########################################################################################################################Function to save a manually entered location
    city_name=entry_city.get().capitalize()                                                                                                     #Get and capitalize the city name from the entry field
    latitude=entry_latitude.get()                                                                                                               #Get the latitude value from the entry field
    longitude=entry_longitude.get()                                                                                                             #Get the longitude value from the entry field
    country_code=entry_country.get().upper()                                                                                                    #Get and uppercase the country code from the entry field
    label=label_combobox.get()                                                                                                                  #Get the label from the combobox
    if not city_name or not latitude or not longitude or not country_code or not label:                                                         #If this statement is true
        messagebox.showerror("Error", "Please fill in all fields.")                                                                             #Show error if any field is empty
        return                                                                                                                                  #Go out the fucntion
    try:                                                                                                                                        #Try this code
        latitude=float(latitude)                                                                                                                #Convert latitude to a float
        longitude=float(longitude)                                                                                                              #Convert longitude to a float
        country_name=pycountry.countries.get(alpha_2=country_code).name if pycountry.countries.get(alpha_2=country_code) else "Unknown country" #Get the full country name based on country code, or "Unknown country" if not found
        text_to_save=(f"{{'name': '{city_name}', 'lon': {longitude}, 'lat': {latitude}, "                                                       #Format the data to save as a JSON-like string
                      f"'label': '{label}', 'country': '{country_name}'}}")                                                                     #Format the data to save as a JSON-like string
        with open('location.txt', 'a') as bestand:                                                                                              #Open the file in append mode
            bestand.write(text_to_save + '\n')                                                                                                  #Write the location data to the file with a newline
        messagebox.showinfo("Success", f"{city_name} has been added manually.")                                                                 #Show success message when data is saved
        load_main_screen()                                                                                                                      #Load the main screen after saving the entry
    except ValueError:                                                                                                                          #If there is an error
        messagebox.showerror("Error", "Latitude and Longitude must be valid numbers.")                                                          #Show error if latitude or longitude is not a valid number

def show_remove_frame():#########Function to display the removal form
    main_frame.pack_forget()    #Hide the main frame
    remove_frame.pack(pady=20)  #Display the remove frame with padding of 20 pixels at the top
    update_country_list()       #Update the country list for the combobox
    country_combobox.current(0) #Set the country combobox to the first item
    update_label_list()         #Update the label list for the combobox
    label_combobox.current(0)   #Set the label combobox to the first item
    update_city_list()          #Update the city list for the combobox

def update_country_list():###################################################Functions to update selection lists
    country_combobox['values']=[]                                           #Clear the current values in the country combobox
    countries=set()                                                         #Initialize an empty set to store unique country names
    try:                                                                    #Try this code
        with open('location.txt', 'r') as bestand:                          #Open the location data file in read mode
            lines=bestand.readlines()                                       #Read all lines from the file
            for line in lines:                                              #If the statement is true
                data=ast.literal_eval(line.strip())                         #Convert each line (a string) to a dictionary
                countries.add(data['country'])                              #Add the country name to the set to ensure uniqueness
        country_combobox['values']=["All places"]+sorted(list(countries))   #Set the combobox values to "All places" plus sorted country names
        update_city_list()                                                  #Call update_city_list to refresh the city list based on the updated countries
    except FileNotFoundError:                                               #If there is an error
        pass                                                                #Do nothing if the file is not found (prevents an error)

def update_label_list():#################################################################Function to update the label selection list
    label_combobox['values']=[]                                                         #Clear current values in the label combobox
    try:                                                                                #Try this code
        with open('labels.txt', 'r') as bestand:                                        #Open the labels file in read mode
            labels=[list(ast.literal_eval(line.strip()).keys())[0] for line in bestand] #Extract label names from each line in the file
        label_combobox['values']=["All labels"]+sorted(labels)                          #Set the combobox values to "All labels" plus sorted labels
        label_combobox.current(0)                                                       #Set the default selection to the first item
    except FileNotFoundError:                                                           #If there is an error
        pass                                                                            #Do nothing if the file is not found (prevents an error)

def update_city_list(event=None):################################################################################################################################Function to update the city list based on selected country and label
    city_listbox.delete(0, tk.END)                                                                                                                              #Clear the current contents of the city listbox
    selected_country=country_combobox.get()                                                                                                                     #Get the selected country from the combobox
    selected_label=label_combobox.get()                                                                                                                         #Get the selected label from the combobox
    try:                                                                                                                                                        #Try this code
        with open('location.txt', 'r') as bestand:                                                                                                              #Open the location data file in read mode
            for line in bestand:                                                                                                                                #Iterate over each line in the file
                data=ast.literal_eval(line.strip())                                                                                                             #Convert the line to a dictionary
                if (selected_country=="All places" or data['country']==selected_country) and (selected_label=="All labels" or data['label']==selected_label):   #Check if the selected country and label match the data or if "All" is selected
                    city_listbox.insert(tk.END, data['name'])                                                                                                   #Insert the city name into the listbox
    except FileNotFoundError:                                                                                                                                   #If there is an error
        pass                                                                                                                                                    #Do nothing if the file is not found (prevents an error)

def remove_city():#######################################################Function to remove the selected city from the list
    selected_city_index=city_listbox.curselection()                     #Get the index of the currently selected city in the listbox
    if not selected_city_index:                                         #If this statement is true
        messagebox.showerror("Error", "Select a place to delete.")      #Show error if no city is selected
        return                                                          #Go out of this function
    selected_city=city_listbox.get(selected_city_index)                 #Get the name of the selected city
    with open('location.txt', 'r') as bestand:                          #Open the location data file in read mode
        lines=bestand.readlines()                                       #Read all lines from the file
    with open('location.txt', 'w') as bestand:                          #Open the file in write mode to overwrite it
        for line in lines:                                              #Iterate through each line in the original file
            if ast.literal_eval(line.strip())['name'] != selected_city: #Check if the line's city name does not match the selected city
                bestand.write(line)                                     #Write the line back to the file if it does not match
    update_city_list()                                                  #Update the city list in the UI to reflect the changes

def load_main_screen():##########Function to return to the main screen
    manual_frame.pack_forget()  #Hide the manual input frame
    remove_frame.pack_forget()  #Hide the removal frame
    main_frame.pack(pady=20)    #Display the main frame with padding of 20 pixels at the top

#############################################Setting up the Tkinter window
root=tk.Tk()                                #Create the main window for the application
root.title("Request Cities Coordinates")    #Set the title of the window to "Request Cities Coordinates"

#########################################################################################################Main frame for city coordinates
main_frame = tk.Frame(root)                                                                             #Create a frame to hold the main content
main_frame.pack(pady=20)                                                                                #Pack the frame into the main window with padding of 20 pixels
label_city = tk.Label(main_frame, text="Enter the name of a place:")                                    #Create a label prompting the user to enter a city name
label_city.pack(pady=10)                                                                                #Pack the label into the main frame with padding of 10 pixels
city_entry = tk.Entry(main_frame, width=50)                                                             #Create an entry field for the city name with a width of 50 characters
city_entry.pack(pady=10)                                                                                #Pack the entry field into the main frame with padding of 10 pixels
label_year = tk.Label(main_frame, text="Choose a label:")                                               #Create a label prompting the user to choose a label
label_year.pack(pady=10)                                                                                #Pack the label into the main frame with padding of 10 pixels
labels = load_labels_from_file('labels.txt')                                                            #Load labels from a file into a list
year_combobox = ttk.Combobox(main_frame, values=labels, state="readonly")                               #Create a combobox for selecting a label, set to read-only
year_combobox.pack(pady=10)                                                                             #Pack the combobox into the main frame with padding of 10 pixels
if labels:                                                                                              #Check if there are any labels available
    year_combobox.current(0)                                                                            #Set the default selected label to the first item if labels exist
fetch_button = tk.Button(main_frame, text="+", command=fetch_location, fg="green", font=("Arial", 20))  #Create a button to fetch location coordinates
fetch_button.pack(pady=20)                                                                              #Pack the button into the main frame with padding of 20 pixels
button_frame = tk.Frame(main_frame)                                                                     #Create a new frame to hold the buttons
button_frame.pack(pady=5)                                                                               #Pack the button frame into the main frame with padding of 5 pixels
manual_button = tk.Button(button_frame, text="Add Place Manually", command=open_manual_add_screen)      #Create a button to open the manual addition screen
manual_button.pack(side=tk.LEFT, padx=5)                                                                #Pack the manual button to the left side with padding of 5 pixels
remove_button = tk.Button(button_frame, text="Delete place", command=show_remove_frame)                 #Create a button to show the remove place frame
remove_button.pack(side=tk.LEFT, padx=5)                                                                #Pack the remove button to the left side with padding of 5 pixels

#####################################################################################Frame for manual entry
manual_frame=tk.Frame(root)                                                         #Create a frame for manual input and associate it with the main window
tk.Label(manual_frame, text="Manual Place Entry", font=("Arial", 14)).pack(pady=10) #Create and pack a label for manual entry with specified font and padding

#####################################Frame for input fields and their labels
input_frame=tk.Frame(manual_frame)  #Create a frame to hold input fields for manual entry
input_frame.pack(pady=10)           #Pack the input frame into the manual frame with padding of 10 pixels

#################################################################################################Place labels and input fields side by side
tk.Label(input_frame, text="Place Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)     #Create a label for the place name and place it in the first row and first column
entry_city=tk.Entry(input_frame, width=40)                                                      #Create an entry field for the city name with a width of 40 characters
entry_city.grid(row=0, column=1, pady=5)                                                        #Place the entry field in the first row and second column with padding
tk.Label(input_frame, text="Latitude:").grid(row=1, column=0, sticky="e", padx=5, pady=5)       #Create a label for the latitude and place it in the second row
entry_latitude=tk.Entry(input_frame, width=40)                                                  #Create an entry field for latitude
entry_latitude.grid(row=1, column=1, pady=5)                                                    #Place the latitude entry field in the second row and second column
tk.Label(input_frame, text="Longitude:").grid(row=2, column=0, sticky="e", padx=5, pady=5)      #Create a label for the longitude and place it in the third row
entry_longitude=tk.Entry(input_frame, width=40)                                                 #Create an entry field for longitude
entry_longitude.grid(row=2, column=1, pady=5)                                                   #Place the longitude entry field in the third row and second column
tk.Label(input_frame, text="Country Code:").grid(row=3, column=0, sticky="e", padx=5, pady=5)   #Create a label for the country code and place it in the fourth row
entry_country=tk.Entry(input_frame, width=40)                                                   #Create an entry field for the country code
entry_country.grid(row=3, column=1, pady=5)                                                     #Place the country code entry field in the fourth row and second column
tk.Label(input_frame, text="Label:").grid(row=4, column=0, sticky="e", padx=5, pady=5)          #Create a label for the label selection and place it in the fifth row
label_combobox=ttk.Combobox(input_frame, values=labels, state="readonly", width=37)             #Create a combobox for selecting labels with specified width and set it to read-only
label_combobox.grid(row=4, column=1, pady=5)                                                    #Place the label combobox in the fifth row and second column

#############################################################################################################Save button and back button for manual frame
tk.Button(manual_frame, text="+", command=save_manual_entry, fg="green", font=("Arial", 20)).pack(pady=20)  #Create a button to save the manual entry, set text color to green, and specify font size; pack it with padding of 20 pixels
tk.Button(manual_frame, text="Back", command=load_main_screen).pack(pady=10)                                #Create a button to return to the main screen and pack it with padding of 10 pixels

#########################################################################################################Frame for deletion
remove_frame=tk.Frame(root)                                                                             #Create a frame for the delete functionality
tk.Label(remove_frame, text="Select a country and city to delete:").pack(pady=10)                       #Create and pack a label prompting the user to select a country and city
combo_frame=tk.Frame(remove_frame)                                                                      #Create a frame to hold the country and label comboboxes
combo_frame.pack(pady=10)                                                                               #Pack the combo frame into the remove frame with padding
country_combobox=ttk.Combobox(combo_frame, state="readonly")                                            #Create a combobox for selecting countries, set to read-only
country_combobox.pack(side=tk.LEFT, padx=(0, 10))                                                       #Pack the country combobox to the left with padding on the right
country_combobox.bind("<<ComboboxSelected>>", lambda event: [update_label_list(), update_city_list()])  #Bind the selection event to update the label and city lists when a country is selected
label_combobox=ttk.Combobox(combo_frame, state="readonly")                                              #Create a combobox for selecting labels, set to read-only
label_combobox.pack(side=tk.LEFT)                                                                       #Pack the label combobox to the left of the country combobox
label_combobox.bind("<<ComboboxSelected>>", update_city_list)                                           #Bind the selection event to update the city list when a label is selected
city_listbox=tk.Listbox(remove_frame, width=50)                                                         #Create a listbox to display cities for deletion with a specified width
city_listbox.pack(pady=10)                                                                              #Pack the city listbox into the remove frame with padding
remove_city_button=tk.Button(remove_frame, text="X", command=remove_city, fg="red", font=("Arial", 20)) #Create a button to remove the selected city, set text color to red and font size
remove_city_button.pack(pady=10)                                                                        #Pack the remove button with padding
tk.Button(remove_frame, text="Back", command=load_main_screen).pack(pady=10)                            #Create a button to return to the main screen and pack it with padding

#############################################################################################Create footer
footer_label=tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))    #Create a label for the footer with creator's name and copyright symbol, using specified font and size
footer_label.pack(side=tk.BOTTOM, pady=10)                                                  #Pack the footer label at the bottom of the window with padding of 10 pixels

root.mainloop() #Start the Tkinter event loop