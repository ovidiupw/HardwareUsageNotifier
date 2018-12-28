import os

import pytest

from hardware_usage_notifier.cli.config.metric import Metric
from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.util.validators import RunnableExceptionValidator

JSON_TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')
SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(JSON_TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')

METRIC_TEST_INSTANCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'metric_test_instances')
METRIC_TEST_INSTANCES_MODULE = 'tests.hardware_usage_notifier.cli.config.metric_test_instances'


@pytest.fixture(scope='function')
def metric_config():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['metric']


def test_when_metric_name_empty_then_exception(metric_config):
    metric_config['name'] = ''
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(metric_config, Monitor.METRICS_DIRECTORY, Monitor.METRIC_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(AssertionError, 'The name of the metric must contain at least one character!')


def test_when_metric_configuration_missing_then_no_exception(metric_config):
    metric_config.pop('configuration')
    Metric(metric_config, Monitor.METRICS_DIRECTORY, Monitor.METRIC_INSTANCES_PARENT_MODULE)


def test_when_metric_file_not_in_directory_then_exception(metric_config):
    metric_config['name'] = 'non_existent_metric.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(
            config=metric_config,
            metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
            metric_parent_module=METRIC_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The metric name must be the Python file name placed in the path '{METRIC_TEST_INSTANCES_DIRECTORY}', "
        f"but got '{metric_config['name']}'!")


def test_when_metric_file_contains_no_python_class_then_exception(metric_config):
    metric_config['name'] = 'no_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(
            config=metric_config,
            metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
            metric_parent_module=METRIC_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The metric defined in '{metric_config['name']}' must have a single class defined in its file, "
        f"but got 0 classes: "
        f"{[]}!")


def test_when_metric_file_contains_multiple_python_classes_then_exception(metric_config):
    metric_config['name'] = 'multiple_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(
            config=metric_config,
            metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
            metric_parent_module=METRIC_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The metric defined in '{metric_config['name']}' must have a single class defined in its file, "
        f"but got 2 classes: "
        f"{['Metric', 'AnotherMetric']}!")


def test_when_metric_class_constructor_missing_configuration_parameter_then_exception(metric_config):
    metric_config['name'] = 'metric_class_constructor_missing_configuration.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(
            config=metric_config,
            metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
            metric_parent_module=METRIC_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"Metric() takes no arguments. Please make sure that the metric class constructor takes a single argument "
        f"representing the metric configuration (which might be empty/undefined)!")


def test_when_metric_class_is_not_subclass_of_abstract_metric_class_then_exception(metric_config):
    metric_config['name'] = 'metric_class_not_subclass_of_abstract_metric_class.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(
            config=metric_config,
            metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
            metric_parent_module=METRIC_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The metric class defined in '{metric_config['name']}' must be a subclass of the abstract Metric class "
        f"defined in {os.path.join(Metric.METRIC_ABSTRACT_CLASS_MODULE, Metric.METRIC_ABSTRACT_CLASS_NAME)}")


def test_when_metric_class_meets_all_contract_requirements_then_no_exception(metric_config):
    metric_config['name'] = 'well_defined_metric.py'
    Metric(
        config=metric_config,
        metric_directory=METRIC_TEST_INSTANCES_DIRECTORY,
        metric_parent_module=METRIC_TEST_INSTANCES_MODULE)
