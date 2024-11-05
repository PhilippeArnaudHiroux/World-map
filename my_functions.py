import requests

def import_data_from_file():                                                    #This function import the data from the location.txt file and put it in a list
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

def import_year_from_file():                                                    #This function import the data from the labels.txt file and put it in a list
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

def get_lat_long_openweathermap(city_name, api_key):                                            #This function asks for the longitude and latitude of a city from openweather
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}" #Construct the API request URL for OpenWeatherMap's geocoding service
    response = requests.get(url)                                                                #Send a GET request to the constructed URL
    data = response.json()                                                                      #Parse the JSON response from the API
    if data:                                                                                    #Check if the response contains any data
        location = data[0]                                                                      #Extract the first location result from the response
        return location['lat'], location['lon']                                                 #Return the latitude and longitude of the location
    else:                                                                                       #If the response does not contains any data
        return None, None                                                                       #Return None if no data is found