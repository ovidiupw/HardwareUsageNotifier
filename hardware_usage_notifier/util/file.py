import json


def create_empty_file(file_path):
    open(file_path, 'a').close()


def read_json_from_file(file_path):
    with open(file_path, 'r') as file_descriptor:
        return json.load(file_descriptor)
