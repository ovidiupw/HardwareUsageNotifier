import os
import click
import jsonschema

from hardware_usage_notifier.cli.config.config import Config

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

SINGLE_MONITOR_CONFIG = os.path.join(TEST_RESOURCES_DIRECTORY, 'single_monitor_config.json')


def test_when_config_read_from_file_then_monitors_initialized_correctly():
    config = Config(click=click, jsonschema=jsonschema)
    config.from_cli_file_path_param(config_file_path=SINGLE_MONITOR_CONFIG)

    assert len(config.monitors) == 1

    monitor = config.monitors[0]
    assert monitor.name == "Monitor_1"
