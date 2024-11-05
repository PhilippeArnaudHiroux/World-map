import tkinter as tk            #Import the tkinter library for creating the GUI
import subprocess               #Import subprocess module to invoke another Python script
from PIL import Image, ImageTk  #Import Image and ImageTk from PIL for working with JPG images and displaying them in the GUI


def open_city_window():######################Define a function to open the city window
    subprocess.Popen(['python', 'city.py']) #Invoke the 'city.py' script as a separate process

def open_year_window():##########################Define a function to open the year window
    subprocess.Popen(['python', 'label.py'])    #Invoke the 'label.py' script as a separate process

def open_map_window():#######################Define a function to open the map window
    subprocess.Popen(['python', 'map.py'])  #Invoke the 'map.py' script as a separate process

#########################Main window setup
root=tk.Tk()            #Create the main application window using Tkinter
root.title("Main menu") #Set the title of the main window to "Main menu"

#################################################################################Load images
city_image=ImageTk.PhotoImage(Image.open("image/city.jpg").resize((100, 100)))  #Load and resize the city image to 100x100 pixels, then convert it to a PhotoImage object
year_image=ImageTk.PhotoImage(Image.open("image/Label.jpg").resize((100, 100))) #Load and resize the label image to 100x100 pixels, then convert it to a PhotoImage object
map_image=ImageTk.PhotoImage(Image.open("image/Map.jpg").resize((100, 100)))    #Load and resize the map image to 100x100 pixels, then convert it to a PhotoImage object

#############################Create a frame for buttons
button_frame=tk.Frame(root) #Create a new frame to hold the buttons
button_frame.pack(pady=20)  #Pack the button frame into the main window with vertical padding of 20 pixels

#####################################################################################Create buttons with images
add_city_button=tk.Button(button_frame, image=city_image, command=open_city_window) #Create a button for adding a city, using the city image and linking to the open_city_window function
add_city_button.grid(row=0, column=0, padx=10)                                      #Place the city button in the grid at row 0, column 0 with horizontal padding of 10 pixels
add_year_button=tk.Button(button_frame, image=year_image, command=open_year_window) #Create a button for adding a year, using the year image and linking to the open_year_window function
add_year_button.grid(row=0, column=1, padx=10)                                      #Place the year button in the grid at row 0, column 1 with horizontal padding of 10 pixels
add_map_button=tk.Button(button_frame, image=map_image, command=open_map_window)    #Create a button for displaying the map, using the map image and linking to the open_map_window function
add_map_button.grid(row=0, column=2, padx=10)                                       #Place the map button in the grid at row 0, column 2 with horizontal padding of 10 pixels

#############################################################################################Create footer
footer_label=tk.Label(root, text="Made by Philippe-Arnaud Hiroux ©", font=("Arial", 10))    #Create a label for the footer with creator's name and copyright symbol, using specified font and size
footer_label.pack(side=tk.BOTTOM, pady=10)                                                  #Pack the footer label at the bottom of the window with padding of 10 pixels

root.mainloop() #Start the Tkinter event loop