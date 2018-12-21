# -*- coding: utf-8 -*-

"""
Defines the Hardware Usage Notifier CLI, by using the 'click' library: https://github.com/pallets/click

Each CLI command and option must be defined separately and then imported and used in this file.

If this file is executed, the __main__ will initialize and start the CLI. However, the CLI might be consumed
as a library by importing the HardwareUsageNotifierCLI object.
"""

import click
import jsonschema

from hardware_usage_notifier.cli import exit_codes
from hardware_usage_notifier.cli.commands.start_monitor import StartMonitor
from hardware_usage_notifier.cli.options.help import Help

CLI_NAME = 'hardware_usage_notifier'
help_option = Help()
CLI_CONTEXT_SETTINGS = dict(help_option_names=[help_option.short_name, help_option.long_name])

start_monitor_command = StartMonitor(click=click, jsonschema=jsonschema)


@click.group(name=CLI_NAME,
             context_settings=CLI_CONTEXT_SETTINGS)
def cli():
    pass


@cli.command(name=start_monitor_command.name)
@click.option(start_monitor_command.config_file.short_name,
              start_monitor_command.config_file.long_name,
              required=start_monitor_command.config_file.required,
              type=start_monitor_command.config_file.type,
              default=start_monitor_command.config_file.default,
              callback=start_monitor_command.config_file.callback)
def start_monitor(config):
    click.echo('Parsed config successfully. Will start monitor. For now, this is just a dummy message')
    exit(exit_codes.SUCCESS_EXIT_CODE)


if __name__ == "__main__":
    cli.add_command(start_monitor)
    cli()
