import tkinter as tk
from tkinter import messagebox
import subprocess  # To invoke another Python script
from PIL import Image, ImageTk  # For working with JPG images

def open_city_window():
    subprocess.Popen(['python', 'city.py'])

def open_year_window():
    subprocess.Popen(['python', 'label.py'])

def open_map_window():
    subprocess.Popen(['python', 'map.py'])

# Main window setup
root = tk.Tk()
root.title("Main menu")

# Load images
city_image = ImageTk.PhotoImage(Image.open("image/city.jpg").resize((100, 100)))
year_image = ImageTk.PhotoImage(Image.open("image/Label.jpg").resize((100, 100)))
map_image = ImageTk.PhotoImage(Image.open("image/Map.jpg").resize((100, 100)))

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Create buttons with images
add_city_button = tk.Button(button_frame, image=city_image, command=open_city_window)
add_city_button.grid(row=0, column=0, padx=10)

add_year_button = tk.Button(button_frame, image=year_image, command=open_year_window)
add_year_button.grid(row=0, column=1, padx=10)

add_map_button = tk.Button(button_frame, image=map_image, command=open_map_window)
add_map_button.grid(row=0, column=2, padx=10)

# Add a label below the buttons
footer_label = tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=10)

# Start the Tkinter event loop
root.mainloop()