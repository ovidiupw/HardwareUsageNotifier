import importlib
import os

from hardware_usage_notifier.util.file import list_classes_in_file
from hardware_usage_notifier.util.validators import FileValidator


class Metric:
    METRICS_FILE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'metrics'))

    def __init__(self, metric_config_dict):
        # TODO validation
        self.name = metric_config_dict['name']
        self.configuration = metric_config_dict.get('configuration')
        self.path = os.path.join(Metric.METRICS_FILE_PATH, self.name)

        assert len(self.name) != 0, 'The name of the metric must contain at least one character!'
        assert FileValidator.is_file_path_valid(file_path=self.path), \
            f"The metric name must be the Python file name placed in the path '{Metric.METRICS_FILE_PATH}, " \
            f"'but got {self.name}'!"

        class_names_in_file = list(map(lambda clazz: clazz.name, list_classes_in_file(self.path)))
        assert FileValidator.does_file_contains_single_class(file_path=self.path), \
            f"The metric defined in '{self.name}' must have a single class defined in its file, " \
            f"but got {len(class_names_in_file)} classes: " \
            f"{class_names_in_file}!"

        try:
            metric_instance_module = importlib.import_module(
                f"hardware_usage_notifier.metrics.{self.name.replace('.py', '')}")
            metric_instance_class = getattr(metric_instance_module, class_names_in_file[0])
            metric_instance = metric_instance_class(self.configuration)

            metric_abstract_class_module = importlib.import_module(f"hardware_usage_notifier.metrics.metric")
            metric_abstract_class_class = getattr(metric_abstract_class_module, 'Metric')
        except Exception as err:
            raise AssertionError(err)

        assert issubclass(type(metric_instance), metric_abstract_class_class), \
            f"The metric class defined in '{self.name}' must be a subclass of the abstract Metric class defined in " \
            f"{os.path.join(Metric.METRICS_FILE_PATH, 'metric.py')}"

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.configuration == other.configuration

    def __hash__(self) -> int:
        return hash((self.name, self.configuration))
