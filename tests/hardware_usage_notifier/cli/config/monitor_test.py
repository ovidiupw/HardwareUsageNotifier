import pytest
import os

from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


@pytest.fixture(scope='function')
def monitor():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]


def test_when_monitor_name_empty_then_exception(monitor):
    monitor['name'] = ''
    exception_validator = RunnableExceptionValidator(lambda: Monitor(monitor))
    exception_validator.verify_exception(AssertionError, 'The name of the monitor must contain at least one character!')


def test_when_monitor_description_missing_then_no_exception(monitor):
    monitor.pop('description')
    Monitor(monitor)
