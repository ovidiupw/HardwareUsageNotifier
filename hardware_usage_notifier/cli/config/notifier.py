import os

from hardware_usage_notifier.util.file import list_class_names_in_file
from hardware_usage_notifier.util.importer import create_object, get_class
from hardware_usage_notifier.util.string import build_module_name
from hardware_usage_notifier.util.validators import FileValidator


class Notifier:
    NOTIFIER_ABSTRACT_CLASS_MODULE = 'hardware_usage_notifier.notifiers.notifier'
    NOTIFIER_ABSTRACT_CLASS_NAME = 'Notifier'

    def __init__(self, config, notifier_directory, notifier_parent_module):
        self.name = config['name']
        self.configuration = config.get('configuration')

        Notifier._assert_notifier_is_abiding_the_contract(
            notifier_file_name=self.name,
            notifier_configuration=self.configuration,
            notifier_directory=notifier_directory,
            notifier_parent_module=notifier_parent_module)

    @staticmethod
    def _assert_notifier_is_abiding_the_contract(
            notifier_file_name, notifier_configuration, notifier_directory, notifier_parent_module):
        """
        Checks if the notifier abides to the contract. If it doesn't abide, it throws an Assertion error with the
        details why the notifier is not compliant. In order for a notifier to abide the contract:

        1.The notifier name must be a valid Python file name, placed in the notifier_directory directory;

        2.The notifier file must have a single class defined in it;

        3.The notifier class must be a subclass of the abstract notifier class defined in the
        NOTIFIER_ABSTRACT_CLASS_MODULE module;

        4.The notifier class must be instantiable. If a configuration dictionary is specified, the instantiation should
        support the configuration as an argument.

        :param notifier_file_name: The file name in which the notifier is defined.
        :param notifier_configuration: A dictionary containing the extra configuration that the notifier might need.
        :param notifier_directory The directory that should contain the file in which the notifier class is defined.
        :param notifier_parent_module The parent of the module that contains the notifier class. For example, if the
        notifier class is defined in the A.B.C module, the parent module is A.B (without the dot between B and C).

        :raises AssertionError: In case any of the notifier definition contract requirements are not met.
        """
        assert len(notifier_file_name) != 0, 'The name of the notifier must contain at least one character!'

        notifier_file_path = os.path.join(notifier_directory, notifier_file_name)
        assert FileValidator.is_file_path_valid(file_path=notifier_file_path), \
            f"The notifier name must be the Python file name placed in the path '{notifier_directory}', " \
                f"but got '{notifier_file_name}'!"

        class_names_in_file = list_class_names_in_file(notifier_file_path)
        assert FileValidator.does_file_contain_single_class(file_path=notifier_file_path), \
            f"The notifier defined in '{notifier_file_name}' must have a single class defined in its file, " \
                f"but got {len(class_names_in_file)} classes: " \
                f"{class_names_in_file}!"

        class_names_in_file = list_class_names_in_file(notifier_file_path)
        try:
            notifier_instance = create_object(
                build_module_name(notifier_parent_module, notifier_file_name),
                class_names_in_file[0],
                notifier_configuration)
            notifier_abstract_class = get_class(
                Notifier.NOTIFIER_ABSTRACT_CLASS_MODULE, Notifier.NOTIFIER_ABSTRACT_CLASS_NAME)
        except TypeError as err:
            raise AssertionError(
                f"{err.args[0]}. Please make sure that the notifier class constructor takes a single argument "
                f"representing the notifier configuration (which might be empty/undefined)!")

        assert issubclass(type(notifier_instance), notifier_abstract_class), \
            f"The notifier class defined in '{notifier_file_name}' must be a subclass of the abstract Notifier class " \
                f"defined in {os.path.join(Notifier.NOTIFIER_ABSTRACT_CLASS_MODULE, Notifier.NOTIFIER_ABSTRACT_CLASS_NAME)}"

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.configuration == other.configuration

    def __hash__(self) -> int:
        return hash((self.name, self.configuration))
