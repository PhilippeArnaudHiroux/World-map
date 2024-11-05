import tkinter as tk                            #Import the tkinter library for creating the GUI
from tkinter import messagebox, colorchooser    #Import specific modules from tkinter for message boxes and color selection
import ast                                      #Import the ast module to safely evaluate string representations of Python literals

def load_labels_from_file(file_name):####################################Define a function to load labels from a specified file
    labels = {}                                                         #Initialize an empty dictionary to store labels and their corresponding colors
    try:                                                                #Try this code
        with open(file_name, 'r') as file:                              #Open the specified file in read mode
            for line in file:                                           #Iterate over each line in the file
                try:                                                    #Try this code
                    data_dict = ast.literal_eval(line.strip())          #Safely evaluate the line as a Python literal
                    for label, color in data_dict.items():              #Iterate over key-value pairs in the dictionary
                        labels[label] = color                           #Store label and color in the labels dictionary
                except (SyntaxError, ValueError):                       #Handle potential errors in evaluation
                    continue                                            #Skip lines that cannot be parsed
    except FileNotFoundError:                                           #Handle the case where the file does not exist
        messagebox.showerror("Error", f"File {file_name} not found.")   #Display an error message
    return labels                                                       #Return the dictionary containing labels and colors

def add_label():#############################################################################Define a function to add a new label
    label = new_label_entry.get().strip()                                                   #Get the label input from the entry field and remove any leading/trailing whitespace
    color_code = color_entry.get().strip()                                                  #Get the color code input from the entry field and remove any leading/trailing whitespace
    if not label or not color_code:                                                         #Check if either the label or color code is empty
        messagebox.showerror("Error", "Please enter both a label and a color code.")        #Display an error message if input is missing
        return                                                                              #Exit the function if inputs are invalid
    with open('labels.txt', 'a') as file:                                                   #Open the labels.txt file in append mode
        color_code = color_code.replace("#", "0x")                                          #Convert color code format from #RRGGBB to 0xRRGGBB
        file.write(f"{{'{label}': '{color_code}'}}\n")                                      #Write the new label and color code in the specified format, ensuring it's on a new line
    update_label_display()                                                                  #Call the function to refresh the display of labels
    new_label_entry.delete(0, tk.END)                                                       #Clear the label entry field after adding
    color_display_label.config(bg="white")                                                  #Reset the background color display to white after adding a label
    messagebox.showinfo("Success", f"Label '{label}' with color code {color_code} added.")  #Display a success message

def update_label_display():######################################################################################Define a function to update the label display
    for widget in label_display_frame.winfo_children():                                                         #Iterate through all widgets in the label display frame
        widget.destroy()                                                                                        #Remove each widget to clear the frame
    labels = load_labels_from_file('labels.txt')                                                                #Load the labels and their colors from the specified file
    for label_name, color in sorted(labels.items()):#                                                           Alphabetical sort by label name
        if isinstance(color, str):                                                                              #Check if the color is a string
            try:                                                                                                #Try this code
                color_code_int = int(color, 16)                                                                 #Convert the string color code from hexadecimal to integer
                color_code_hex = f"#{color_code_int:06X}"                                                       #Convert the integer back to a hex string in #RRGGBB format
            except ValueError:                                                                                  #If there is an error
                continue                                                                                        #Skip this label if conversion fails (invalid color format)
        else:                                                                                                   #If the color is not a string
            continue                                                                                            #Skip if color format is not a string
        label_widget = tk.Label(label_display_frame, text=label_name, bg=color_code_hex, width=20, anchor='w')  #Create a label widget with the label name and background color
        label_widget.pack(pady=2)                                                                               #Add the label to the frame with some vertical padding for spacing

def choose_color():##############################################Define a function to choose a color
    color_code = colorchooser.askcolor(title="Choose a color")  #Open the color chooser dialog
    if color_code[1] is not None:                               #Check if the user selected a color
        hex_color = color_code[1]                               #Get the hex color code from the color chooser
        color_entry.delete(0, tk.END)                           #Clear the current entry in the color entry field
        color_entry.insert(0, hex_color)                        #Insert the selected hex color code into the entry field
        color_display_label.config(bg=hex_color)                #Change the background color of the color display label
        choose_color_button.config(bg=hex_color, fg="white")    #Change the button's background and text color
    else:                                                       #If there is no color selected
        messagebox.showinfo("Information", "No color selected.")#Show an info message if no color was selected

def switch_to_delete_frame():####Define a function to switch to the delete frame
    add_frame.pack_forget()     #Hide the add label frame
    delete_frame.pack(pady=10)  #Show the delete label frame
    load_labels_for_deletion()  #Load labels for deletion

def switch_to_add_frame():#######Define a function to switch to the add frame
    delete_frame.pack_forget()  #Hide the delete label frame
    add_frame.pack(pady=10)     #Show the add label frame
    update_label_display()      #Refresh label display in add frame

def load_labels_for_deletion():######################################################################################################Define a function to load labels for deletion
    for widget in checkbox_frame.winfo_children():                                                                                  #Clear existing checkboxes and colored labels
        widget.destroy()                                                                                                            #Destroy the widget
    labels = load_labels_from_file('labels.txt')                                                                                    #Load existing labels
    global label_vars                                                                                                               #Declare globally to access in delete_labels function
    label_vars = {}                                                                                                                 #Initialize a dictionary to store checkbox variables
    for label_name, color in sorted(labels.items()):                                                                                #Alphabetical sort by label name
        var = tk.IntVar()                                                                                                           #Create an IntVar for checkbox state tracking
        label_vars[label_name] = var                                                                                                #Store the variable for each checkbox
        checkbox_frame_inner = tk.Frame(checkbox_frame)                                                                             #Create a frame for the checkbox and colored label
        checkbox_frame_inner.pack(anchor='w')                                                                                       #Pack the inner frame for label and checkbox alignment
        checkbox = tk.Checkbutton(checkbox_frame_inner, text="", variable=var)                                                      #No text for checkbox
        checkbox.pack(side='left')                                                                                                  #Place checkbox on the left        
        if isinstance(color, str):                                                                                                  #Determine the color for the colored label
            try:                                                                                                                    #Try is code
                color_code_int = int(color, 16)                                                                                     #Convert string color code to integer
                color_code_hex = f"#{color_code_int:06X}"                                                                           #Convert the color code to a hex string
            except ValueError:                                                                                                      #If there is an error
                color_code_hex = "white"                                                                                            #Default to white if conversion fails
        else:                                                                                                                       #If the statement is not true
            color_code_hex = "white"                                                                                                #Default to white for invalid color formats
        colored_label = tk.Label(checkbox_frame_inner, text=label_name, bg=color_code_hex, width=20, anchor='w', relief="groove")   #Create a colored label with the label name inside
        colored_label.pack(side='left', padx=5)                                                                                     #Place the colored label next to the checkbox

def delete_labels():##################################################################### Een functie om labels te verwijderen
    labels_to_delete = [label for label, var in label_vars.items() if var.get() == 1]   # Maak een lijst van te verwijderen labels op basis van de geselecteerde checkboxen
    if not labels_to_delete:                                                            # Toon een foutmelding als er geen labels zijn geselecteerd voor verwijdering
        messagebox.showerror("Error", "Selecteer alstublieft ten minste één label om te verwijderen.")  # Toon een foutmeldingsvenster
        return                                                                          # Verlaat de functie als er geen labels zijn geselecteerd
    
    labels = load_labels_from_file('labels.txt')                                        # Laad bestaande labels uit het bestand
    for selected_label in labels_to_delete:                                             # Verwijder de geselecteerde labels uit de dictionary
        if selected_label in labels:                                                    # Controleer of het geselecteerde label bestaat in de geladen labels
            del labels[selected_label]                                                  # Verwijder het geselecteerde label uit de labels dictionary
    
    with open('labels.txt', 'w') as file:                                               # Schrijf de bijgewerkte labels terug naar het bestand 
        for label, color in labels.items():                                             # Itereer door elk label en de bijbehorende kleur
            file.write(f"{{'{label}': '{color}'}}\n")                                   # Schrijf het label en de kleur naar het bestand met een nieuwe regel aan het einde

    load_labels_for_deletion()                                                          # Roep de functie aan om de checkboxen te vernieuwen
    messagebox.showinfo("Success", f"Verwijderde labels: {', '.join(labels_to_delete)}.")   # Toon een succesbericht met de namen van de verwijderde labels

#############################Set up the Tkinter window
root = tk.Tk()              #Create the main window for the application
root.title("Manage Labels") #Set the title of the window

#############################Frame for adding labels
add_frame = tk.Frame(root)  #Create a frame widget to hold the components for adding labels
add_frame.pack(pady=10)     #Add the frame to the main window with padding on the Y-axis

#################################################################Create a label and entry for adding a new label
label_new_label = tk.Label(add_frame, text="Add a new label:")  #Create a label widget with the text "Add a new label"
label_new_label.pack(pady=10)                                   #Pack the label into the add_frame with vertical padding of 10 pixels
new_label_entry = tk.Entry(add_frame, width=20)                 #Create an entry widget for user input with a width of 20 characters
new_label_entry.pack(pady=10)                                   #Pack the entry widget into the add_frame with vertical padding of 10 pixels
color_entry = tk.Entry(add_frame, width=20)                     #Create another entry widget for entering a color code, also with a width of 20 characters

#################################################################################################Create a button to open the color chooser
choose_color_button = tk.Button(add_frame, text="Choose Color", command=choose_color, width=20) #Create a button that, when clicked, will invoke the choose_color function to open a color picker
choose_color_button.pack(pady=5)                                                                #Pack the button into the add_frame with vertical padding of 5 pixels

#########################################################################################################Create a button to add the new label and color
add_label_button = tk.Button(add_frame, text="+", command=add_label, fg="green", font=("Arial", 20))    #Create a button for adding a new label with a green foreground color and larger font
add_label_button.pack(pady=20)                                                                          #Pack the button into the add_frame with vertical padding of 20 pixels

#####################################################################################################################Create a label for displaying the selected color
color_display_label = tk.Label(add_frame, text="Selected Color", width=20, height=2, bg="white", relief="groove")   #Create a label to display the selected color with a white background and a grooved border

#############################################Frame for displaying existing labels
label_display_frame = tk.Frame(add_frame)   #Create a new frame to hold the existing labels and their colors
label_display_frame.pack(pady=10)           #Pack the label display frame into the add_frame with vertical padding of 10 pixels

#################################Frame for deleting labels
delete_frame = tk.Frame(root)   #Create a new frame that will contain all elements related to label deletion, placed within the main application window (root)

#########################################Frame for checkboxes
checkbox_frame = tk.Frame(delete_frame) #Create a frame specifically for holding the checkboxes that allow users to select which labels to delete
checkbox_frame.pack(pady=10)            #Pack the checkbox frame into the delete_frame with vertical padding of 10 pixels to separate it from other elements

#############################################################################################################Create a button to switch to the delete frame
switch_frame_button = tk.Button(add_frame, text="Switch to Delete Labels", command=switch_to_delete_frame)  #This button, when clicked, will call the function to switch to the delete frame, allowing the user to manage label deletions.
switch_frame_button.pack(pady=10)                                                                           #Pack the button into the add_frame with vertical padding of 10 pixels for spacing.

#########################################################################################################Create a button to delete the selected labels
delete_button = tk.Button(delete_frame, text="X", command=delete_labels, fg="red", font=("Arial", 20))  #This button, styled with a red foreground and larger font, will call the function to delete selected labels when clicked.
delete_button.pack(pady=20)                                                                             #Pack the delete button into the delete_frame with vertical padding of 20 pixels for spacing.

#################################################################################################Create a button to go back to the add labels frame
back_button = tk.Button(delete_frame, text="Back to Add Labels", command=switch_to_add_frame)   #This button allows the user to switch back to the frame where they can add new labels.
back_button.pack(pady=5)                                                                        #Pack the back button into the delete_frame with vertical padding of 5 pixels for spacing.

#############################################################################################Create footer
footer_label=tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))    #Create a label for the footer with creator's name and copyright symbol, using specified font and size
footer_label.pack(side=tk.BOTTOM, pady=10)                                                  #Pack the footer label at the bottom of the window with padding of 10 pixels

#############################Start with the delete frame hidden
delete_frame.pack_forget()  #Initially hide the delete_frame so that users start in the add frame.

#########################Initial display of labels
update_label_display()  #Call the function to load and display existing labels in the add frame.

#################Run the Tkinter event loop
root.mainloop() #Start the Tkinter event loop to wait for user interactions.