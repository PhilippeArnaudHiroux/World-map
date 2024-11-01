import tkinter as tk
from tkinter import messagebox, colorchooser, ttk
import ast  # To safely evaluate string representations of Python literals

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

def add_year():
    new_year = new_year_entry.get()
    color_code = color_entry.get().strip()

    if not new_year or not color_code:
        messagebox.showerror("Fout", "Vul zowel een jaar als een kleurcode in.")
        return
    
    # Append new year and color to year.txt
    with open('year.txt', 'a') as file:
        file.write(f"{{'{new_year}': {color_code}}}\n")  # Ensure that it's on a new line
    
    # Refresh the year combobox
    update_year_combobox()
    new_year_entry.delete(0, tk.END)
    color_display_label.config(bg="white")  # Reset to white after adding a year
    messagebox.showinfo("Succes", f"Jaar {new_year} met kleurcode {color_code} is toegevoegd.")

def update_year_combobox():
    # Update the combobox with years from the file
    years = load_years_from_file('year.txt')
    year_combobox['values'] = years
    if years:
        year_combobox.current(0)  # Select the first year if available

def choose_color():
    color_code = colorchooser.askcolor(title="Kies een kleur")
    if color_code[1] is not None:  # Check if the user selected a color
        # Get the hexadecimal color code from the RGB tuple
        hex_color = color_code[1]
        color_entry.delete(0, tk.END)  # Clear the entry field
        color_entry.insert(0, hex_color)  # Insert the hex color code
        color_display_label.config(bg=hex_color)  # Change the label's background color to the selected color
        choose_color_button.config(bg=hex_color, fg="white")  # Change the button's background color to the selected color
    else:
        messagebox.showinfo("Informatie", "Geen kleur geselecteerd.")  # Inform user if no color was chosen

# Set up the Tkinter window
root = tk.Tk()
root.title("Voeg Nieuw Jaar Toe")

# Create a label and entry for adding a new year
label_new_year = tk.Label(root, text="Voeg een nieuw jaar toe:")
label_new_year.pack(pady=10)

new_year_entry = tk.Entry(root, width=20)
new_year_entry.pack(pady=10)

# Create an entry to display the color code
color_entry = tk.Entry(root, width=20)

# Create a button to open the color chooser
choose_color_button = tk.Button(root, text="Choose a color", command=choose_color, width=20)
choose_color_button.pack(pady=5)

# Create a button to add the new year and color
add_year_button = tk.Button(root, text="Voeg Jaar Toe", command=add_year)
add_year_button.pack(pady=20)

# Create a label for displaying the selected color
color_display_label = tk.Label(root, text="Gekozen kleur", width=20, height=2, bg="white", relief="groove")

# Create a label for displaying available years
label_years = tk.Label(root, text="Bestaande jaren:")
label_years.pack(pady=10)

# Create a combobox to display existing years
year_combobox = ttk.Combobox(root, state="readonly")
year_combobox.pack(pady=10)

# Load existing years into the combobox at startup
update_year_combobox()

# Voeg een label toe onder de knoppen
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)  # Plaats het label onderaan met wat ruimte

# Run the Tkinter event loop
root.mainloop()
