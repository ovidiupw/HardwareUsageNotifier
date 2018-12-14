# -*- coding: utf-8 -*-

import click

from hardware_usage_notifier.common import exit_codes

CLI_NAME = 'hardware_usage_notifier'
START_MONITOR_COMMAND_NAME = 'start-monitor'


@click.group(name=CLI_NAME)
def cli():
    pass


@cli.command(name=START_MONITOR_COMMAND_NAME)
def start_monitor():
    click.echo('Will start monitor. For now, this is just a dummy message')
    exit(exit_codes.SUCCESS_EXIT_CODE)


if __name__ == "__main__":
    cli.add_command(start_monitor)
    cli()
