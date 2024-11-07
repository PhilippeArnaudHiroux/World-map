import requests                 #Import the requests library to handle HTTP requests
from tkinter import messagebox  #Import specific modules from tkinter for message boxes and themed widgets
import ast                      #Import ast module to safely evaluate string representations of Python literals
import pycountry                #Import pycountry to work with country information and codes
from api_key import api_key

def import_data_from_file():#####################################################This function import the data from the location.txt file and put it in a list
    data_list = []                                                              #Create an empty list to store the data dictionaries
    with open("location.txt", 'r') as file:                                     #Open the file 'location.txt' in read mode
        for line in file:                                                       #Iterate through each line in the file
            line = line.strip()                                                 #Remove white space from the beginning and end of the line
            if line:                                                            #Process only non-empty lines
                try:                                                            #Convert the string to a dictionary using eval
                    data = eval(line)                                           #Use eval() here to evaluate the line as a Python expression
                    if isinstance(data, dict):                                  #Verify that the result is a dictionary
                        data_list.append(data)                                  #Append the dictionary to the data_list
                    else:                                                       #If the the result is not a dictionary
                        print(f"Rule is not a dictionary: {line}")              #Print a message if it's not a dictionary
                except (SyntaxError, ValueError) as e:                          #Catch syntax errors or value errors in eval
                    print(f"Error processing rule: {line}. Error message: {e}") #Print an error message if parsing fails              
    return data_list                                                            #Return the list of dictionaries after reading all lines

def import_labels_from_file():###################################################This function import the data from the labels.txt file and put it in a list
    data_list = []                                                              #Initialize an empty list to store the data dictionaries
    with open("labels.txt", 'r') as file:                                       #Open the file 'labels.txt' in read mode
        for line in file:                                                       #Iterate through each line in the file
            line = line.strip()                                                 #Remove white space from the beginning and end of the line
            if line:                                                            #Process only non-empty lines
                try:                                                            #Convert the string to a dictionary using eval
                    data = eval(line)                                           #Use eval() here to evaluate the line as a Python expression
                    if isinstance(data, dict):                                  #Verify that the result is a dictionary
                        data_list.append(data)                                  #Append the dictionary to data_list
                    else:                                                       #If the the result is not a dictionary
                        print(f"Rule is not a dictionary: {line}")              #Print a message if it is not a dictionary
                except (SyntaxError, ValueError) as e:                          #Handle syntax or value errors in eval
                    print(f"Error processing rule: {line}. Error message: {e}") #Print an error message if parsing fails      
    return data_list                                                            #Return the list of dictionaries after reading all lines

def get_lat_long_openweathermap(city_name):#############################################################################################################This function asks for the longitude and latitude of a city from OpenWeather
    url=f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"                                                           #Construct the API request URL for OpenWeatherMap's geocoding service
    response=requests.get(url)                                                                                                                          #Send a GET request to the constructed URL
    data=response.json()                                                                                                                                #Parse the JSON response from the API
    if data:                                                                                                                                            #Check if the response contains any data
        location=data[0]                                                                                                                                #Extract the first location result from the response
        country_code=location['country']                                                                                                                #Get the country code from the location data
        country_name=pycountry.countries.get(alpha_2=country_code).name if pycountry.countries.get(alpha_2=country_code) else "Unknown country code"    #Retrieve the country name using the country code, handle case of unknown country code
        return location['lat'], location['lon'], country_name                                                                                           #Return the latitude and longitude of the location along with the country name
    else:                                                                                                                                               #If the response does not contain any data
        return None, None                                                                                                                               #Return None if no data is found

def load_labels_from_file(file_name):####################################This function loads the years as a label from 'labels.txt'
    years = []                                                          #Initialize an empty list to store the years
    try:                                                                #Try this code
        with open(file_name, 'r') as file:                              #Open the specified file in read mode
            for line in file:                                           #Iterate through each line in the file
                try:                                                    #Convert string representation of dictionary to a Python dictionary
                    data_dict = ast.literal_eval(line.strip())          #Safely evaluate the line as a dictionary
                    for year in data_dict.keys():                       #Iterate through keys (years) in the dictionary
                        years.append(year)                              #Add only the year to the list
                except (SyntaxError, ValueError):                       #Handle parsing errors
                    continue                                            #Skip lines that cannot be parsed
    except FileNotFoundError:                                           #Handle the case where the file does not exist
        messagebox.showerror("Error", f"File {file_name} not found.")   #Display an error message if file is missing
    years.sort()                                                        #Sort the list of years in ascending order
    return years                                                        #Return the sorted list of years