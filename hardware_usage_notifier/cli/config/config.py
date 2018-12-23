import json
import os

import click as click_library
import jsonschema as jsonschema_library

from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.cli.config.monitor import Monitor


class Config(object):
    monitors = []

    def __init__(self, click, jsonschema):
        assert type(click) == type(click_library), \
            "The 'click' argument must be the imported click library"
        assert type(jsonschema) == type(jsonschema_library), \
            "The 'jsonschema' argument must be the imported jsonschema library"
        self.click = click
        self.jsonschema = jsonschema

    def from_cli_file_path_param(self, cli_context=None, param_name=None, config_file_path=None):
        if not os.path.isfile(config_file_path):
            raise self.click.BadParameter('The supplied config file path must exist and not be a directory.')

        try:
            config_json = read_json_from_file(config_file_path)
        except json.JSONDecodeError as err:
            raise self.click.BadParameter(
                f"Could not parse JSON file at '{os.path.abspath(config_file_path)}'. Failure at line '{err.lineno}', "
                f"column '{err.colno}': '{err.msg}'."
            )

        try:
            self.jsonschema.validate(config_json, self._read_config_json_schema())
        except self.jsonschema.exceptions.ValidationError as err:
            raise self.click.BadParameter(
                f"Error parsing config file at '{os.path.abspath(config_file_path)}', path '{list(err.absolute_path)}':"
                f" '{err.args[0]}'."
            )

        for monitor_config_dict in config_json['monitors']:
            try:
                monitor = Monitor(monitor_config_dict)
            except AssertionError as err:
                raise self.click.BadParameter(
                    f"Error initializing monitor from configuration:\n"
                    f"{json.dumps(monitor_config_dict)}\n\n"
                    f"{err.args[0]}"
                )
            self.monitors.append(monitor)

        self._assert_unique_monitor_names(self.monitors, config_file_path)

        return self

    def __eq__(self, other: object) -> bool:
        return self.monitors == other.monitors

    def __hash__(self) -> int:
        return hash(self.monitors)

    def _read_config_json_schema(self):
        json_schema_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config_file_json_schema.json')
        return read_json_from_file(json_schema_path)

    def _assert_unique_monitor_names(self, monitors, config_file_path):
        monitor_names = map(lambda monitor: monitor.name, monitors)
        unique_monitor_names = set()
        for monitor_name in monitor_names:
            if monitor_name in unique_monitor_names:
                raise self.click.BadParameter(
                    f"Error parsing config file at '{os.path.abspath(config_file_path)}': "
                    f"Duplicate monitor names are not allowed. However, detected duplicate name '{monitor_name}'!"
                )
            unique_monitor_names.add(monitor_name)
