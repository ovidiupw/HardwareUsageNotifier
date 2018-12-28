import os

from hardware_usage_notifier.util.file import list_class_names_in_file
from hardware_usage_notifier.util.importer import create_object, get_class
from hardware_usage_notifier.util.string import build_module_name
from hardware_usage_notifier.util.validators import FileValidator


class Threshold:
    COMPARATOR_ABSTRACT_CLASS_MODULE = 'hardware_usage_notifier.comparators.comparator'
    COMPARATOR_ABSTRACT_CLASS_NAME = 'Comparator'

    def __init__(self, config, comparator_directory, comparator_parent_module):
        self.comparator = config['comparator']
        self.value = config['value']
        self.alarm_points = int(config['alarm_points'])
        self.clear_points = int(config['clear_points'])

        Threshold._assert_threshold_comparator_is_abiding_the_contract(
            comparator_file_name=self.comparator,
            comparator_reference_value=self.value,
            comparator_directory=comparator_directory,
            comparator_parent_module=comparator_parent_module)

        assert self.alarm_points > 0, \
            f"The threshold alarm points must be a positive integer, but got '{self.alarm_points}'!"
        assert self.clear_points > 0, \
            f"The threshold clear points must be a positive integer, but got '{self.clear_points}'!"

    @staticmethod
    def _assert_threshold_comparator_is_abiding_the_contract(
            comparator_file_name, comparator_reference_value, comparator_directory, comparator_parent_module):
        """
        Checks if the comparator abides to the contract. If it doesn't abide, it throws an Assertion error with the
        details why the comparator is not compliant. In order for a comparator to abide the contract:

        1.The comparator name must be a valid Python file name, placed in the comparator_directory directory;

        2.The comparator file must have a single class defined in it;

        3.The comparator class must be a subclass of the abstract comparator class defined in the
        COMPARATOR_ABSTRACT_CLASS_NAME module;

        4.The comparator class must be instantiable. The comparator constructor must take a single argument representing
        the reference value (comparator_reference_value) for the comparison.

        :param comparator_file_name: The file name in which the comparator is defined.
        :param comparator_reference_value: The reference value which the comparator will evaluate against.
        :param comparator_directory The directory that should contain the file in which the comparator class is defined.
        :param comparator_parent_module The parent of the module that contains the comparator class. For example, if the
        comparator class is defined in the A.B.C module, the parent module is A.B (without the dot between B and C).

        :raises AssertionError: In case any of the comparator definition contract requirements are not met.
        """
        assert len(comparator_file_name) != 0, 'The threshold comparator must contain at least one character!'

        comparator_file_path = os.path.join(comparator_directory, comparator_file_name)
        assert FileValidator.is_file_path_valid(file_path=comparator_file_path), \
            f"The comparator name must be the Python file name placed in the path '{comparator_directory}', " \
                f"but got '{comparator_file_name}'!"

        class_names_in_file = list_class_names_in_file(comparator_file_path)
        assert FileValidator.does_file_contain_single_class(file_path=comparator_file_path), \
            f"The comparator defined in '{comparator_file_name}' must have a single class defined in its file, " \
                f"but got {len(class_names_in_file)} classes: " \
                f"{class_names_in_file}!"

        class_names_in_file = list_class_names_in_file(comparator_file_path)
        try:
            comparator_instance = create_object(
                build_module_name(comparator_parent_module, comparator_file_name),
                class_names_in_file[0],
                comparator_reference_value)
            comparator_abstract_class = get_class(
                Threshold.COMPARATOR_ABSTRACT_CLASS_MODULE, Threshold.COMPARATOR_ABSTRACT_CLASS_NAME)
        except TypeError as err:
            raise AssertionError(
                f"{err.args[0]}. Please make sure that the comparator class constructor takes a single argument "
                f"representing the reference value for the comparison operation!")
        except Exception as err:
            raise AssertionError(err)

        assert issubclass(type(comparator_instance), comparator_abstract_class), \
            f"The comparator class defined in '{comparator_file_name}' must be a subclass of the abstract Comparator " \
            f"class defined in" \
            f" {os.path.join(Threshold.COMPARATOR_ABSTRACT_CLASS_MODULE, Threshold.COMPARATOR_ABSTRACT_CLASS_NAME)}"

    def __eq__(self, other: object) -> bool:
        return self.comparator == other.comparator \
               and self.value == other.value \
               and self.alarm_points == other.alarm_points \
               and self.clear_points == other.clear_points

    def __hash__(self) -> int:
        return hash((self.comparator, self.value, self.alarm_points, self.clear_points))
