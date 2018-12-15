import json
import os
import click


class Config(object):

    @staticmethod
    def from_cli_file_path_param(cli_context, param_name, config_file_path):
        if not os.path.isfile(config_file_path):
            raise click.BadParameter('The supplied config file path must exist and not be a directory.')

        with open(config_file_path, 'r') as config_file_descriptor:
            try:
                config_json = json.load(config_file_descriptor)
            except json.JSONDecodeError as err:
                raise click.BadParameter(
                    f"\'Could not parse JSON file at '{config_file_path}'. Failure at line '{err.lineno}', "
                    f"column '{err.colno}': '{err.msg}'."
                )

        click.echo(f"JSON file that was read: {config_json}")
        return config_json
