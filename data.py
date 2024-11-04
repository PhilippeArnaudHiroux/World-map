def import_data_from_file():
    data_list = []
    
    with open("location.txt", 'r') as file:
        for line in file:
            line = line.strip()  # Verwijder witruimtes aan het begin en einde van de regel
            if line:  # Alleen niet-lege regels verwerken
                try:
                    # Verander de string naar een dictionary door gebruik te maken van eval
                    data = eval(line)  # Gebruik eval() hier
                    if isinstance(data, dict):  # Verifieer dat het een dictionary is
                        data_list.append(data)
                    else:
                        print(f"Rule is not a dictionary: {line}")
                except (SyntaxError, ValueError) as e:
                    print(f"Error processing rule: {line}. Error message: {e}")               
    return data_list

def import_year_from_file():
    data_list = []
    
    with open("labels.txt", 'r') as file:
        for line in file:
            line = line.strip()  # Verwijder witruimtes aan het begin en einde van de regel
            if line:  # Alleen niet-lege regels verwerken
                try:
                    # Verander de string naar een dictionary door gebruik te maken van eval
                    data = eval(line)  # Gebruik eval() hier
                    if isinstance(data, dict):  # Verifieer dat het een dictionary is
                        data_list.append(data)
                    else:
                        print(f"Rule is not a dictionary: {line}")
                except (SyntaxError, ValueError) as e:
                    print(f"Error processing rule: {line}. Error message: {e}")        
    return data_list