# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner

from hardware_usage_notifier.cli import exit_codes
from hardware_usage_notifier.cli.commands.start_monitor import StartMonitor
from hardware_usage_notifier.cli.hardware_usage_notifier import cli
from hardware_usage_notifier.cli.options.help import Help
from hardware_usage_notifier.util.file import create_empty_file
from hardware_usage_notifier.util.string import string_contains

start_monitor_command = StartMonitor()
help_option = Help()


@pytest.fixture(scope='function')
def cli_runner():
    return CliRunner()


def test_when_no_argument_then_error(cli_runner):
    with cli_runner.isolated_filesystem():
        no_args_command_result = cli_runner.invoke(cli,
                                                   [start_monitor_command.name])

        assert no_args_command_result.exit_code == exit_codes.INVALID_ARGUMENT_EXIT_CODE
        assert string_contains(no_args_command_result.output,
                               f" Invalid value for \"{start_monitor_command.config_file.short_name}\" / \"{start_monitor_command.config_file.long_name}\": The supplied config file path must exist and not be a directory.")


def test_when_short_help_then_same_output_as_long_help(cli_runner):
    short_help_command_result = cli_runner.invoke(cli,
                                                  [start_monitor_command.name, help_option.short_name])
    long_help_command_result = cli_runner.invoke(cli,
                                                 [start_monitor_command.name, help_option.long_name])

    assert short_help_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert long_help_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert short_help_command_result.output == long_help_command_result.output


def test_when_default_name_config_file_exists_and_is_empty_then_error(cli_runner):
    with cli_runner.isolated_filesystem():
        create_empty_file(start_monitor_command.config_file.default)
        command_result = cli_runner.invoke(cli, [
            start_monitor_command.name,
            start_monitor_command.config_file.short_name,
            start_monitor_command.config_file.default
        ])
        assert command_result.exit_code == exit_codes.INVALID_ARGUMENT_EXIT_CODE
        assert string_contains(command_result.output,
                               f"Could not parse JSON file at '{start_monitor_command.config_file.default}'. Failure at line '1', column '1':")


def test_when_config_file_exists_and_is_empty_then_error(cli_runner):
    config_file_name = 'my-config-file.json'
    with cli_runner.isolated_filesystem():
        create_empty_file(config_file_name)
        command_result = cli_runner.invoke(cli, [
            start_monitor_command.name,
            start_monitor_command.config_file.short_name,
            config_file_name
        ])
        assert command_result.exit_code == exit_codes.INVALID_ARGUMENT_EXIT_CODE
        assert string_contains(command_result.output,
                               f"Could not parse JSON file at '{config_file_name}'. Failure at line '1', column '1':")
