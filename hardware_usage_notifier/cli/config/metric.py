import os

from hardware_usage_notifier.util.file import list_class_names_in_file
from hardware_usage_notifier.util.importer import create_object, get_class
from hardware_usage_notifier.util.validators import FileValidator


class Metric:
    METRIC_ABSTRACT_CLASS_MODULE = 'hardware_usage_notifier.metrics.metric'
    METRIC_ABSTRACT_CLASS_NAME = 'Metric'

    def __init__(self, config, metric_directory, metric_parent_module):
        self.name = config['name']
        self.configuration = config.get('configuration')

        Metric._assert_metric_is_abiding_the_contract(
            metric_file_name=self.name,
            metric_configuration=self.configuration,
            metric_directory=metric_directory,
            metric_parent_module=metric_parent_module)

    @staticmethod
    def _assert_metric_is_abiding_the_contract(
            metric_file_name, metric_configuration, metric_directory, metric_parent_module):
        """
        Checks if the metric abides to the contract. If it doesn't abide, it throws an Assertion error with the details
        why the metric is not compliant. In order for a metric to abide the contract:

        1.The metric name must be a valid Python file name, placed in the metric_directory directory;

        2.The metric file must have a single metric class defined in it;

        3.The metric class must be a subclass of the abstract metric class defined in the metric_module_prefix module;

        4.The metric class must be instantiable. If a configuration dictionary is specified, the instantiation should
        support the configuration as an argument.

        :param metric_file_name: The file name in which the metric is defined.
        :param metric_configuration: A dictionary containing the extra configuration that the metric might need.
        :param metric_directory The directory that should contain the file in which the metric class is defined.
        :param metric_parent_module The parent of the module that contains the metric class. For example, if the metric
        class is defined in the A.B.C module, the parent module is A.B (without the dot between B and C).

        :raises AssertionError: In case any of the metric definition contract requirements are not met.
        """
        metric_file_path = Metric._build_metric_file_path(metric_file_name, metric_directory)

        assert len(metric_file_name) != 0, 'The name of the metric must contain at least one character!'
        assert FileValidator.is_file_path_valid(file_path=metric_file_path), \
            f"The metric name must be the Python file name placed in the path '{metric_directory}, " \
                f"'but got {metric_file_name}'!"

        class_names_in_file = list_class_names_in_file(metric_file_path)
        assert FileValidator.does_file_contain_single_class(file_path=metric_file_path), \
            f"The metric defined in '{metric_file_name}' must have a single class defined in its file, " \
                f"but got {len(class_names_in_file)} classes: " \
                f"{class_names_in_file}!"

        class_names_in_file = list_class_names_in_file(metric_file_path)
        try:
            metric_instance = create_object(
                Metric._build_metric_module_name(metric_file_name, metric_parent_module),
                class_names_in_file[0],
                metric_configuration)
            metric_abstract_class = get_class(Metric.METRIC_ABSTRACT_CLASS_MODULE, Metric.METRIC_ABSTRACT_CLASS_NAME)
        except Exception as err:
            raise AssertionError(err)

        assert issubclass(type(metric_instance), metric_abstract_class), \
            f"The metric class defined in '{metric_file_name}' must be a subclass of the abstract Metric class " \
                f"defined in {os.path.join(metric_directory, 'metric.py')}"

    @staticmethod
    def _build_metric_file_path(metric_file_name, metric_directory):
        return os.path.join(metric_directory, metric_file_name)

    @staticmethod
    def _build_metric_module_name(metric_file_name, metric_parent_module):
        return f"{metric_parent_module}.{metric_file_name.replace('.py', '')}"

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.configuration == other.configuration

    def __hash__(self) -> int:
        return hash((self.name, self.configuration))
