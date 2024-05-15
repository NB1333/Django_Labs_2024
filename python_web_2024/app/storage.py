import json
import os

def load_data(filepath):
    # Check if the file exists and is not empty
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        # Initialize with default structure if the file doesn't exist or is empty
        data = {'users': [], 'transactions': []}
        with open(filepath, 'w') as file:
            json.dump(data, file)
    
    # Ensure all necessary keys exist in data
    data.setdefault('users', [])
    data.setdefault('transactions', [])
    
    return data



def save_data(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
