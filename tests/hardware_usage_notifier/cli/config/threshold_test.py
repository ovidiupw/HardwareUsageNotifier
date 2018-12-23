import pytest
import os

from hardware_usage_notifier.cli.config.threshold import Threshold
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


@pytest.fixture(scope='function')
def threshold():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['threshold']


def test_when_comparator_empty_then_exception(threshold):
    threshold['comparator'] = ''
    exception_validator = RunnableExceptionValidator(lambda: Threshold(threshold))
    exception_validator.verify_exception(
        AssertionError, 'The threshold comparator must contain at least one character!')


def test_when_alarm_points_not_positive_integer_then_exception(threshold):
    threshold['alarm_points'] = 0
    exception_validator = RunnableExceptionValidator(lambda: Threshold(threshold))
    exception_validator.verify_exception(
        AssertionError, "The threshold alarm points must be a positive integer, but got '0'!")


def test_when_alarm_points_positive_integer_then_no_exception(threshold):
    threshold['alarm_points'] = 1
    Threshold(threshold)


def test_when_clear_points_not_positive_integer_then_exception(threshold):
    threshold['clear_points'] = 0
    exception_validator = RunnableExceptionValidator(lambda: Threshold(threshold))
    exception_validator.verify_exception(
        AssertionError, "The threshold clear points must be a positive integer, but got '0'!")


def test_when_clear_points_positive_integer_then_no_exception(threshold):
    threshold['clear_points'] = 1
    Threshold(threshold)
