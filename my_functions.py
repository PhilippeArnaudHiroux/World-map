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
                    else:
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
                    else:
                        print(f"Rule is not a dictionary: {line}")              #Print a message if it is not a dictionary
                except (SyntaxError, ValueError) as e:                          #Handle syntax or value errors in eval
                    print(f"Error processing rule: {line}. Error message: {e}") #Print an error message if parsing fails      
    return data_list                                                            #Return the list of dictionaries after reading all lines

