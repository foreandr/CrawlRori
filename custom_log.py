import json
import os

def log_to_file(data, file_path):
    # Ensure the file exists; create if not
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    # Read existing data from file
    current_data = read_from_file(file_path)

    # If data is a list, process each item; otherwise, treat it as a single dictionary
    if isinstance(data, list):
        for item in data:
            process_entry(item, current_data)
    else:
        process_entry(data, current_data)

    # Write updated data back to file
    with open(file_path, 'w') as file:
        json.dump(current_data, file, indent=4)

def process_entry(data, current_data):
    # Extract the main key from the data to log
    main_key = list(data.keys())[0]
    
    # Check if the key already exists
    found = False
    for entry in current_data:
        if main_key in entry:
            # If it exists, modify the entry
            entry[main_key] = data[main_key]
            found = True
            break

    # If not found, append the new data
    if not found:
        current_data.append(data)

def read_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
