import os

import pytest

from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.cli.config.threshold import Threshold
from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.util.validators import RunnableExceptionValidator

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')
SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')

COMPARATORS_TEST_INSTANCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'comparators_test_instances')
COMPARATORS_TEST_INSTANCES_MODULE = 'tests.hardware_usage_notifier.cli.config.comparators_test_instances'


@pytest.fixture(scope='function')
def threshold_config():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['threshold']


def test_when_comparator_empty_then_exception(threshold_config):
    threshold_config['comparator'] = ''
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=Monitor.COMPARATORS_DIRECTORY,
            comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(
        AssertionError, 'The threshold comparator must contain at least one character!')


def test_when_alarm_points_not_positive_integer_then_exception(threshold_config):
    threshold_config['alarm_points'] = 0
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=Monitor.COMPARATORS_DIRECTORY,
            comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(
        AssertionError, "The threshold alarm points must be a positive integer, but got '0'!")


def test_when_alarm_points_positive_integer_then_no_exception(threshold_config):
    threshold_config['alarm_points'] = 1
    Threshold(
        config=threshold_config,
        comparator_directory=Monitor.COMPARATORS_DIRECTORY,
        comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE)


def test_when_clear_points_not_positive_integer_then_exception(threshold_config):
    threshold_config['clear_points'] = 0
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=Monitor.COMPARATORS_DIRECTORY,
            comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(
        AssertionError, "The threshold clear points must be a positive integer, but got '0'!")


def test_when_clear_points_positive_integer_then_no_exception(threshold_config):
    threshold_config['clear_points'] = 1
    Threshold(
        config=threshold_config,
        comparator_directory=Monitor.COMPARATORS_DIRECTORY,
        comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE)


def test_when_comparator_file_not_in_directory_then_exception(threshold_config):
    threshold_config['comparator'] = 'non_existent_comparator.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
            comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The comparator name must be the Python file name placed in the path '{COMPARATORS_TEST_INSTANCES_DIRECTORY}',"
        f" but got '{threshold_config['comparator']}'!")


def test_when_comparator_file_contains_no_python_class_then_exception(threshold_config):
    threshold_config['comparator'] = 'no_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
            comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The comparator defined in '{threshold_config['comparator']}' must have a single class defined in its file, "
        f"but got 0 classes: "
        f"{[]}!")


def test_when_comparator_file_contains_multiple_python_classes_then_exception(threshold_config):
    threshold_config['comparator'] = 'multiple_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
            comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The comparator defined in '{threshold_config['comparator']}' must have a single class defined in its file, "
        f"but got 2 classes: "
        f"{['Comparator', 'AnotherComparator']}!")


def test_when_comparator_class_constructor_missing_reference_value_parameter_then_exception(threshold_config):
    threshold_config['comparator'] = 'comparator_class_constructor_missing_reference_value.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
            comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"Comparator() takes no arguments. Please make sure that the comparator class constructor takes a single "
        f"argument representing the reference value for the comparison operation!")


def test_when_comparator_class_is_not_subclass_of_abstract_comparator_class_then_exception(threshold_config):
    threshold_config['comparator'] = 'comparator_class_not_subclass_of_abstract_comparator_class.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Threshold(
            config=threshold_config,
            comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
            comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The comparator class defined in '{threshold_config['comparator']}' must be a subclass of the abstract "
        f"Comparator class defined in "
        f"{os.path.join(Threshold.COMPARATOR_ABSTRACT_CLASS_MODULE, Threshold.COMPARATOR_ABSTRACT_CLASS_NAME)}")


def test_when_comparator_class_meets_all_contract_requirements_then_no_exception(threshold_config):
    threshold_config['comparator'] = 'well_defined_comparator.py'
    Threshold(
        config=threshold_config,
        comparator_directory=COMPARATORS_TEST_INSTANCES_DIRECTORY,
        comparator_parent_module=COMPARATORS_TEST_INSTANCES_MODULE)
