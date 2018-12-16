import json
import os

import click

from hardware_usage_notifier.util.file import read_json_from_file


class Config(object):

    @staticmethod
    def from_cli_file_path_param(cli_context, param_name, config_file_path):
        if not os.path.isfile(config_file_path):
            raise click.BadParameter('The supplied config file path must exist and not be a directory.')

        try:
            config_json = read_json_from_file(config_file_path)
        except json.JSONDecodeError as err:
            raise click.BadParameter(
                f"\'Could not parse JSON file at '{config_file_path}'. Failure at line '{err.lineno}', "
                f"column '{err.colno}': '{err.msg}'."
            )

        click.echo(f"JSON file that was read: {config_json}")
        return config_json
