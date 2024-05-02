import json
import logging

logging.basicConfig(filename='url_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_existing_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return {item['url'] for item in data}
    except FileNotFoundError:
        return set()

def append_to_json(data, filename):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)