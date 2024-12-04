import json
import os

def log_to_file(data, file_path="./data.json"):
    """
    Logs data into a JSON file. Ensures no duplicate entries are added.
    """
    ensure_directory_exists(file_path)

    # Initialize the file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False)

    # Load existing data
    current_data = read_from_file(file_path)

    # Process new data
    if isinstance(data, list):
        for item in data:
            process_entry(item, current_data)
    else:
        process_entry(data, current_data)

    # Save updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(current_data, file, indent=4, ensure_ascii=False)

def ensure_directory_exists(file_path):
    """
    Ensures the directory for the given file exists; creates it if not.
    """
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

def process_entry(entry, current_data):
    """
    Adds an entry to the current data if it is not already present.
    """
    if entry not in current_data:  # Avoid adding duplicates
        current_data.append(entry)

def read_from_file(file_path):
    """
    Reads and parses JSON data from a file. Returns an empty list if the file is missing or invalid.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []