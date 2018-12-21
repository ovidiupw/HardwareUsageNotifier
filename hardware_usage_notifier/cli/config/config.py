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
            self.jsonschema.validate(config_json, Config.read_config_json_schema())
        except self.jsonschema.exceptions.ValidationError as err:
            raise self.click.BadParameter(
                f"Error parsing config file at '{os.path.abspath(config_file_path)}', path '{list(err.absolute_path)}':"
                f" '{err.message}'."
            )

        for monitor_config_dict in config_json['monitors']:
            monitor = Monitor(monitor_config_dict)
            self.monitors.append(monitor)

        return self

    @staticmethod
    def read_config_json_schema():
        json_schema_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config_file_json_schema.json')
        return read_json_from_file(json_schema_path)
