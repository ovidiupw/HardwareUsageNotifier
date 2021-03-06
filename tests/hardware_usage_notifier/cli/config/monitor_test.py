import os

import pytest

from hardware_usage_notifier.cli.config.interval import Interval
from hardware_usage_notifier.cli.config.metric import Metric
from hardware_usage_notifier.cli.config.monitor import Monitor
from hardware_usage_notifier.cli.config.threshold import Threshold
from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.util.validators import RunnableExceptionValidator

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')

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


def test_when_monitor_well_formed_then_no_exception(monitor):
    monitor_instance = Monitor(monitor)
    assert monitor_instance.name == monitor['name']
    assert monitor_instance.description == monitor['description']
    assert monitor_instance.interval == Interval(monitor['interval'])
    assert monitor_instance.metric == Metric(
        config=monitor['metric'],
        metric_directory=Monitor.METRICS_DIRECTORY,
        metric_parent_module=Monitor.METRIC_INSTANCES_PARENT_MODULE)
    assert monitor_instance.threshold == Threshold(
        config=monitor['threshold'],
        comparator_directory=Monitor.COMPARATORS_DIRECTORY,
        comparator_parent_module=Monitor.COMPARATOR_INSTANCES_PARENT_MODULE)
    assert monitor_instance.notifiers == Monitor.Notifiers(
        notifiers_config_dict=monitor['notifiers'],
        notifier_directory=Monitor.NOTIFIERS_DIRECTORY,
        notifier_parent_module=Monitor.NOTIFIER_INSTANCES_PARENT_MODULE)
