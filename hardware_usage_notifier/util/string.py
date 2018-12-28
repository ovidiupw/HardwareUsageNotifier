def string_contains(string, substring):
    return string.find(substring) != -1


def build_module_name(parent_module_name, python_file_name):
    return f"{parent_module_name}.{python_file_name.replace('.py', '')}"
