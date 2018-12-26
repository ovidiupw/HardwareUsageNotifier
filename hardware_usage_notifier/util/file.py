import json
import ast


def create_empty_file(file_path):
    open(file_path, 'a').close()


def create_file(file_path, file_content):
    with open(file_path, 'w') as file_descriptor:
        file_descriptor.write(file_content)


def read_json_from_file(file_path):
    with open(file_path, 'r') as file_descriptor:
        return json.load(file_descriptor)


def list_classes_in_file(file_path):
    with open(file_path) as file_descriptor:
        node = ast.parse(file_descriptor.read())
        return [n for n in node.body if isinstance(n, ast.ClassDef)]


def list_class_names_in_file(file_path):
    return list(map(lambda clazz: clazz.name, list_classes_in_file(file_path)))
