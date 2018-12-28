import os

import pytest

from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.cli.config.threshold import Threshold
from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.util.validators import RunnableExceptionValidator

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


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
