import os
import click
import jsonschema
import json

from hardware_usage_notifier.cli.config.config import Config
from hardware_usage_notifier.util.validators import RunnableExceptionValidator
from hardware_usage_notifier.util.file import read_json_from_file

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'json_test_instances')

SINGLE_MONITOR_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')
DUPLICATE_MONITOR_NAMES_CONFIG_FILE_NAME = os.path.join(TEST_RESOURCES_DIRECTORY, 'duplicate_monitor_names_config.json')
NEGATIVE_ALARM_POINTS_CONFIG_FILE_NAME = os.path.join(
    TEST_RESOURCES_DIRECTORY, 'negative_alarm_points_monitor_config.json')


def test_when_config_read_from_file_then_monitors_initialized_correctly():
    config = Config(click=click, jsonschema=jsonschema)
    config.from_cli_file_path_param(config_file_path=SINGLE_MONITOR_CONFIG_FILE_NAME)

    assert len(config.monitors) == 1

    monitor = config.monitors[0]
    assert monitor.name == 'Monitor_1'
    assert monitor.description == 'A description for Monitor_1'
    assert monitor.metric.name == 'example_metric.py'
    assert monitor.metric.configuration['some_dummy_config_A'] == ['1', '2', '3']
    assert monitor.threshold.comparator == 'example_comparator.py'
    assert monitor.threshold.value == '999'
    assert monitor.threshold.alarm_points == 3
    assert monitor.threshold.clear_points == 1
    assert monitor.interval.minutes == 5
    assert monitor.notifiers.monitor_alarm.name == 'example_notifier_1.py'
    assert monitor.notifiers.monitor_alarm.configuration['some_dummy_config_B'] == '123'
    assert monitor.notifiers.monitor_failure.name == 'example_notifier_2.py'
    assert monitor.notifiers.monitor_failure.configuration['some_dummy_config_C'] == '123'


def test_when_config_contains_duplicate_monitor_names_then_exception():
    config = Config(click=click, jsonschema=jsonschema)

    exception_validator = RunnableExceptionValidator(
        lambda: config.from_cli_file_path_param(config_file_path=DUPLICATE_MONITOR_NAMES_CONFIG_FILE_NAME))
    exception_validator.verify_exception(
        click.BadParameter,
        f"Error parsing config file at '{os.path.abspath(DUPLICATE_MONITOR_NAMES_CONFIG_FILE_NAME)}': "
        f"Duplicate monitor names are not allowed. However, detected duplicate name 'Monitor_1'!"
    )


def test_when_config_monitor_invalid_then_exception():
    config = Config(click=click, jsonschema=jsonschema)
    expected_monitor_config = read_json_from_file(NEGATIVE_ALARM_POINTS_CONFIG_FILE_NAME)['monitors'][0]

    exception_validator = RunnableExceptionValidator(
        lambda: config.from_cli_file_path_param(config_file_path=NEGATIVE_ALARM_POINTS_CONFIG_FILE_NAME))
    exception_validator.verify_exception(
        click.BadParameter,
        f"Error initializing monitor from configuration:\n"
        f"{json.dumps(expected_monitor_config)}\n"
        f"The threshold alarm points must be a positive integer, but got '-5'!"
    )
