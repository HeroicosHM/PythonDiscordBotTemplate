# Library to manage json data format.
import json

def save_data(file, data):
    # Open file and write data to it.
    with open(file, 'w+', encoding = "utf-8") as save_file:
        try:
            save_file.write(json.dumps(data, indent = 2))
        except Exception as e:
            print('Could not save data: ' + str(e))

def load_data(file):
    # Open file and return data loaded from it.
    with open(file, 'r', encoding = "utf-8") as load_file:
        return json.loads(load_file.read())
