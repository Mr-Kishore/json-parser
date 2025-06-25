import os

def read_json_file(filepath):
    if not filepath.lower().endswith(".json"):
        raise ValueError("Only .json files are supported")

    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
