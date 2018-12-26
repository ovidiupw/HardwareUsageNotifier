import pytest
import os

from hardware_usage_notifier.cli.config.metric import Metric
from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


@pytest.fixture(scope='function')
def metric():
    return read_json_from_file(SINGLE_MONITOR_CONFIG_FILE_NAME)['monitors'][0]['metric']


def test_when_metric_name_empty_then_exception(metric):
    metric['name'] = ''
    exception_validator = RunnableExceptionValidator(
        lambda: Metric(metric, Monitor.METRICS_DIRECTORY, Monitor.METRIC_INSTANCES_PARENT_MODULE))
    exception_validator.verify_exception(AssertionError, 'The name of the metric must contain at least one character!')


def test_when_metric_configuration_missing_then_no_exception(metric):
    metric.pop('configuration')
    Metric(metric, Monitor.METRICS_DIRECTORY, Monitor.METRIC_INSTANCES_PARENT_MODULE)
