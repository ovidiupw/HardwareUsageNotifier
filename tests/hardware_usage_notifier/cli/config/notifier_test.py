import pytest
import os

from hardware_usage_notifier.cli.config.notifier import Notifier
from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')
SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')

NOTIFIERS_TEST_INSTANCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'notifiers_test_instances')
NOTIFIERS_TEST_INSTANCES_MODULE = 'tests.hardware_usage_notifier.cli.config.notifiers_test_instances'


@pytest.fixture(scope='function')
def notifier_config():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['notifiers']['monitor_alarm']


def test_when_notifier_name_empty_then_exception(notifier_config):
    notifier_config['name'] = ''
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(notifier_config, Monitor.NOTIFIERS_DIRECTORY, Monitor.NOTIFIER_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(
        AssertionError, 'The name of the notifier must contain at least one character!')


def test_when_notifier_monitor_alarm_configuration_missing_then_no_exception(notifier_config):
    notifier_config.pop('configuration')
    Notifier(notifier_config, Monitor.NOTIFIERS_DIRECTORY, Monitor.NOTIFIER_INSTANCES_PARENT_MODULE)


def test_when_notifier_monitor_failure_configuration_missing_then_no_exception(notifier_config):
    notifier_config.pop('configuration')
    Notifier(notifier_config, Monitor.NOTIFIERS_DIRECTORY, Monitor.NOTIFIER_INSTANCES_PARENT_MODULE)


def test_when_notifier_file_not_in_directory_then_exception(notifier_config):
    notifier_config['name'] = 'non_existent_notifier.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(
            config=notifier_config,
            notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
            notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The notifier name must be the Python file name placed in the path '{NOTIFIERS_TEST_INSTANCES_DIRECTORY}',"
        f" but got '{notifier_config['name']}'!")


def test_when_comparator_file_contains_no_python_class_then_exception(notifier_config):
    notifier_config['name'] = 'no_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(
            config=notifier_config,
            notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
            notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The notifier defined in '{notifier_config['name']}' must have a single class defined in its file, "
        f"but got 0 classes: "
        f"{[]}!")


def test_when_notifier_file_contains_multiple_python_classes_then_exception(notifier_config):
    notifier_config['name'] = 'multiple_classes_in_file.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(
            config=notifier_config,
            notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
            notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The notifier defined in '{notifier_config['name']}' must have a single class defined in its file, "
        f"but got 2 classes: "
        f"{['Notifier', 'AnotherNotifier']}!")


def test_when_comparator_class_constructor_missing_reference_value_parameter_then_exception(notifier_config):
    notifier_config['name'] = 'notifier_class_constructor_missing_configuration.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(
            config=notifier_config,
            notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
            notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"Notifier() takes no arguments. Please make sure that the notifier class constructor takes a single "
        f"argument representing the notifier configuration (which might be empty/undefined)!")


def test_when_comparator_class_is_not_subclass_of_abstract_comparator_class_then_exception(notifier_config):
    notifier_config['name'] = 'notifier_class_not_subclass_of_abstract_notifier_class.py'
    exception_validator = RunnableExceptionValidator(
        lambda: Notifier(
            config=notifier_config,
            notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
            notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE))
    exception_validator.verify_exception(
        AssertionError,
        f"The notifier class defined in '{notifier_config['name']}' must be a subclass of the abstract "
        f"Notifier class defined in "
        f"{os.path.join(Notifier.NOTIFIER_ABSTRACT_CLASS_MODULE, Notifier.NOTIFIER_ABSTRACT_CLASS_NAME)}")


def test_when_comparator_class_meets_all_contract_requirements_then_no_exception(notifier_config):
    notifier_config['name'] = 'well_defined_notifier.py'
    Notifier(
        config=notifier_config,
        notifier_directory=NOTIFIERS_TEST_INSTANCES_DIRECTORY,
        notifier_parent_module=NOTIFIERS_TEST_INSTANCES_MODULE)
