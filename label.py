import tkinter as tk
from tkinter import messagebox, colorchooser, ttk
import ast  # To safely evaluate string representations of Python literals

def load_labels_from_file(file_name):
    labels = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                try:
                    data_dict = ast.literal_eval(line.strip())
                    for label, color in data_dict.items():
                        labels[label] = color  # Store label and color in a dictionary
                except (SyntaxError, ValueError):
                    continue  # Skip lines that cannot be parsed
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_name} not found.")
    return labels

def add_label():
    label = new_label_entry.get().strip()
    color_code = color_entry.get().strip()

    if not label or not color_code:
        messagebox.showerror("Error", "Please enter both a label and a color code.")
        return
    
    # Append new label and color to labels.txt
    with open('labels.txt', 'a') as file:
        color_code = color_code.replace("#", "0x")
        file.write(f"\n{{'{label}': '{color_code}'}}")  # Ensure it's on a new line
    
    # Refresh the label display
    update_label_display()
    new_label_entry.delete(0, tk.END)
    color_display_label.config(bg="white")  # Reset to white after adding a label
    messagebox.showinfo("Success", f"Label '{label}' with color code {color_code} added.")

def update_label_display():
    # Clear existing labels
    for label in label_labels:
        label.destroy()
    label_labels.clear()

    # Load labels from the file
    labels = load_labels_from_file('labels.txt')
    
    # Create labels for existing labels with their corresponding colors
    for label_name, color in sorted(labels.items()):  # Alphabetical sort by label name
        # Controleer of color een string is
        if isinstance(color, str):
            try:
                color_code_int = int(color, 16)  # Convert string color code to integer
                color_code_hex = f"#{color_code_int:06X}"  # Convert the color code to a hex string
            except ValueError:
                print(f"Error converting color '{color}' to integer. Skipping this label.")
                continue  # Skips this label if conversion fails
        else:
            print(f"Invalid color format for label '{label_name}': {color}. Skipping this label.")
            continue

        label = tk.Label(label_frame, text=label_name, bg=color_code_hex, width=20, anchor='w')
        label.pack(pady=2)  # Add some padding for spacing
        label_labels.append(label)


def choose_color():
    color_code = colorchooser.askcolor(title="Choose a color")
    if color_code[1] is not None:  # Check if the user selected a color
        hex_color = color_code[1]
        color_entry.delete(0, tk.END)
        color_entry.insert(0, hex_color)
        color_display_label.config(bg=hex_color)
        choose_color_button.config(bg=hex_color, fg="white")
    else:
        messagebox.showinfo("Information", "No color selected.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Add New Label")

# Create a label and entry for adding a new label
label_new_label = tk.Label(root, text="Add a new label:")
label_new_label.pack(pady=10)

new_label_entry = tk.Entry(root, width=20)
new_label_entry.pack(pady=10)

# Create a label and entry for RGB color code
label_color = tk.Label(root, text="Choose an RGB color:")

color_entry = tk.Entry(root, width=20)

# Create a button to open the color chooser
choose_color_button = tk.Button(root, text="Choose Color", command=choose_color, width=20)
choose_color_button.pack(pady=5)

# Create a button to add the new label and color
add_label_button = tk.Button(root, text="Add Label", command=add_label)
add_label_button.pack(pady=20)

# Create a label for displaying the selected color
color_display_label = tk.Label(root, text="Selected Color", width=20, height=2, bg="white", relief="groove")

# Create a frame for displaying existing labels
label_frame = tk.Frame(root)
label_frame.pack(pady=10)

label_labels = []  # List to keep track of label labels
update_label_display()  # Load existing labels into the display at startup

# Add a footer label
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Run the Tkinter event loop
root.mainloop()
