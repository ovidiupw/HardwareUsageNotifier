# -*- coding: utf-8 -*-

"""
Defines the Hardware Usage Notifier CLI, by using the 'click' library: https://github.com/pallets/click

Each CLI command and option must be defined separately and then imported and used in this file.

If this file is executed, the __main__ will initialize and start the CLI. However, the CLI might be consumed
as a library by importing the HardwareUsageNotifierCLI object.
"""

import click
import click_log
import jsonschema
import os

from hardware_usage_notifier.cli import exit_codes
from hardware_usage_notifier.cli.commands.start_monitor import StartMonitor
from hardware_usage_notifier.cli.options.help import Help
from hardware_usage_notifier.util.logging import build_production_logger, build_test_logger

CLI_NAME = 'hardware_usage_notifier'
HELP_OPTION = Help()
CLI_CONTEXT_SETTINGS = dict(help_option_names=[HELP_OPTION.short_name, HELP_OPTION.long_name])
START_MONITOR_COMMAND = StartMonitor(click=click, jsonschema=jsonschema)

try:
    if os.environ['RUN_ENV'] == 'test':
        LOG = build_test_logger()
    else:
        LOG = build_production_logger()
except KeyError:
    LOG = build_production_logger()


@click.group(name=CLI_NAME,
             context_settings=CLI_CONTEXT_SETTINGS)
@click_log.simple_verbosity_option(LOG)
def cli():
    LOG.info("Initializing CLI...")
    pass


@cli.command(name=START_MONITOR_COMMAND.name)
@click.option(START_MONITOR_COMMAND.config_file.short_name,
              START_MONITOR_COMMAND.config_file.long_name,
              required=START_MONITOR_COMMAND.config_file.required,
              type=START_MONITOR_COMMAND.config_file.type,
              default=START_MONITOR_COMMAND.config_file.default,
              callback=START_MONITOR_COMMAND.config_file.callback)
@click_log.simple_verbosity_option(LOG)
def start_monitor(config):
    LOG.info('Parsed config successfully. Will start monitor. For now, this is just a dummy message')
    exit(exit_codes.SUCCESS_EXIT_CODE)


if __name__ == "__main__":
    cli.add_command(start_monitor)
    cli()
