# -*- coding: utf-8 -*-

"""
Defines the Hardware Usage Notifier CLI, by using the 'click' library: https://github.com/pallets/click

Each CLI command and option must be defined separately and then imported and used in this file.

If this file is executed, the __main__ will initialize and start the CLI. However, the CLI might be consumed
as a library by importing the HardwareUsageNotifierCLI object.
"""

import os

import click
import click_log
import jsonschema
import atexit

from hardware_usage_notifier.cli import exit_codes
from hardware_usage_notifier.cli.commands.start_monitor import StartMonitor
from hardware_usage_notifier.cli.options.help import Help
from hardware_usage_notifier.util.logging import LOGGER_ID
from hardware_usage_notifier.util.logging \
    import build_production_logger, build_test_logger, cleanup_empty_log_files, shut_down_loggers

CLI_NAME = 'hardware_usage_notifier'

_HELP_OPTION = Help()
_CLI_CONTEXT_SETTINGS = dict(help_option_names=[_HELP_OPTION.short_name, _HELP_OPTION.long_name])
_START_MONITOR_COMMAND = StartMonitor(click=click, jsonschema=jsonschema)
_WAIT_BEFORE_CLEANUP_SECONDS = 2

try:
    if os.environ['RUN_ENV'] == 'test':
        _LOG = build_test_logger()
    else:
        _LOG = build_production_logger()
except KeyError:
    _LOG = build_production_logger()


@click.group(name=CLI_NAME,
             context_settings=_CLI_CONTEXT_SETTINGS)
@click_log.simple_verbosity_option(_LOG)
@click.pass_context
def cli(context):
    # Make logger available for each sub-command of the CLI; Found as context.meta[LOGGER]
    context.meta[LOGGER_ID] = _LOG
    context.meta[LOGGER_ID].info("Initializing CLI...")
    pass


@cli.command(name=_START_MONITOR_COMMAND.name)
@click.option(_START_MONITOR_COMMAND.config_file.short_name,
              _START_MONITOR_COMMAND.config_file.long_name,
              required=_START_MONITOR_COMMAND.config_file.required,
              type=_START_MONITOR_COMMAND.config_file.type,
              default=_START_MONITOR_COMMAND.config_file.default,
              callback=_START_MONITOR_COMMAND.config_file.callback)
@click.pass_context
def start_monitor(context, config):
    context.meta[LOGGER_ID] \
        .info('Parsed config successfully. Will start monitor. For now, this is just a dummy message')
    exit(exit_codes.SUCCESS_EXIT_CODE)


if __name__ == "__main__":
    cli.add_command(start_monitor)
    cli()

atexit.register(cleanup_empty_log_files, directory='./')
atexit.register(shut_down_loggers)
