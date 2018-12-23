import pytest
import os

from hardware_usage_notifier.cli.config.notifier import Notifier
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


@pytest.fixture(scope='function')
def notifier():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['metric']


def test_when_notifier_name_empty_then_exception(notifier):
    notifier['name'] = ''
    exception_validator = RunnableExceptionValidator(lambda: Notifier(notifier))
    exception_validator.verify_exception(
        AssertionError, 'The name of the notifier must contain at least one character!')


def test_when_notifier_configuration_missing_then_no_exception(notifier):
    notifier.pop('configuration')
    Notifier(notifier)
