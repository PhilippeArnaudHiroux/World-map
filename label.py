import tkinter as tk
from tkinter import messagebox, colorchooser
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
    # Clear existing label display
    for widget in label_display_frame.winfo_children():
        widget.destroy()

    # Load labels from the file
    labels = load_labels_from_file('labels.txt')
    
    # Create labels for existing labels with their corresponding colors
    for label_name, color in sorted(labels.items()):  # Alphabetical sort by label name
        if isinstance(color, str):
            try:
                color_code_int = int(color, 16)  # Convert string color code to integer
                color_code_hex = f"#{color_code_int:06X}"  # Convert the color code to a hex string
            except ValueError:
                continue  # Skip this label if conversion fails
        else:
            continue  # Skip if color format is invalid

        label_widget = tk.Label(label_display_frame, text=label_name, bg=color_code_hex, width=20, anchor='w')
        label_widget.pack(pady=2)  # Add some padding for spacing

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

def switch_to_delete_frame():
    add_frame.pack_forget()  # Hide the add label frame
    delete_frame.pack(pady=10)  # Show the delete label frame
    load_labels_for_deletion()  # Load labels for deletion

def switch_to_add_frame():
    delete_frame.pack_forget()  # Hide the delete label frame
    add_frame.pack(pady=10)  # Show the add label frame
    update_label_display()  # Refresh label display in add frame

def load_labels_for_deletion():
    # Clear existing checkboxes and colored labels
    for widget in checkbox_frame.winfo_children():
        widget.destroy()

    # Load existing labels
    labels = load_labels_from_file('labels.txt')

    # Create checkboxes for each label
    global label_vars  # Declare globally to access in delete_labels function
    label_vars = {}
    
    for label_name, color in sorted(labels.items()):  # Alphabetical sort by label name
        var = tk.IntVar()
        label_vars[label_name] = var  # Store the variable for each checkbox
        
        # Create a frame for the checkbox and colored label
        checkbox_frame_inner = tk.Frame(checkbox_frame)
        checkbox_frame_inner.pack(anchor='w')  # Pack the inner frame for label and checkbox alignment

        checkbox = tk.Checkbutton(checkbox_frame_inner, text="", variable=var)  # No text for checkbox
        checkbox.pack(side='left')  # Place checkbox on the left

        # Determine the color for the colored label
        if isinstance(color, str):
            try:
                color_code_int = int(color, 16)  # Convert string color code to integer
                color_code_hex = f"#{color_code_int:06X}"  # Convert the color code to a hex string
            except ValueError:
                color_code_hex = "white"  # Default to white if conversion fails
        else:
            color_code_hex = "white"  # Default to white for invalid color formats

        # Create a colored label with the label name inside
        colored_label = tk.Label(checkbox_frame_inner, text=label_name, bg=color_code_hex, width=20, anchor='w', relief="groove")
        colored_label.pack(side='left', padx=5)  # Place the colored label next to the checkbox

def delete_labels():
    labels_to_delete = [label for label, var in label_vars.items() if var.get() == 1]

    if not labels_to_delete:
        messagebox.showerror("Error", "Please select at least one label to delete.")
        return
    
    # Load existing labels
    labels = load_labels_from_file('labels.txt')

    # Remove the selected labels
    for selected_label in labels_to_delete:
        if selected_label in labels:
            del labels[selected_label]
    
    # Write updated labels back to file
    with open('labels.txt', 'w') as file:
        for label, color in labels.items():
            file.write(f"\n{{'{label}': '{color}'}}")

    load_labels_for_deletion()  # Refresh the checkboxes
    messagebox.showinfo("Success", f"Deleted labels: {', '.join(labels_to_delete)}.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Manage Labels")

# Frame for adding labels
add_frame = tk.Frame(root)
add_frame.pack(pady=10)

# Create a label and entry for adding a new label
label_new_label = tk.Label(add_frame, text="Add a new label:")
label_new_label.pack(pady=10)

new_label_entry = tk.Entry(add_frame, width=20)
new_label_entry.pack(pady=10)

color_entry = tk.Entry(add_frame, width=20)

# Create a button to open the color chooser
choose_color_button = tk.Button(add_frame, text="Choose Color", command=choose_color, width=20)
choose_color_button.pack(pady=5)

# Create a button to add the new label and color
add_label_button = tk.Button(add_frame, text="Add Label", command=add_label)
add_label_button.pack(pady=20)

# Create a label for displaying the selected color
color_display_label = tk.Label(add_frame, text="Selected Color", width=20, height=2, bg="white", relief="groove")

# Frame for displaying existing labels
label_display_frame = tk.Frame(add_frame)
label_display_frame.pack(pady=10)

# Frame for deleting labels
delete_frame = tk.Frame(root)

# Frame for checkboxes
checkbox_frame = tk.Frame(delete_frame)
checkbox_frame.pack(pady=10)

# Create a button to switch to the delete frame
switch_frame_button = tk.Button(add_frame, text="Switch to Delete Labels", command=switch_to_delete_frame)
switch_frame_button.pack(pady=10)

# Create a button to delete the selected labels
delete_button = tk.Button(delete_frame, text="Delete Selected Labels", command=delete_labels)
delete_button.pack(pady=20)

# Create a button to go back to the add labels frame
back_button = tk.Button(delete_frame, text="Back to Add Labels", command=switch_to_add_frame)
back_button.pack(pady=5)

# Create a footer label
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Start with the delete frame hidden
delete_frame.pack_forget()  # Hide delete frame initially

# Initial display of labels
update_label_display()

# Run the Tkinter event loop
root.mainloop()
