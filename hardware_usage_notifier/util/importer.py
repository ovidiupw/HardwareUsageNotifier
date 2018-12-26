import importlib


def create_object(module_name, class_name, *constructor_arguments):
    module = importlib.import_module(module_name)
    clazz = getattr(module, class_name)
    return clazz(constructor_arguments)


def get_class(module_name, class_name):
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
