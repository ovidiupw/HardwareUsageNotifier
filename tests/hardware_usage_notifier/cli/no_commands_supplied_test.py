# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner

from hardware_usage_notifier.cli.hardware_usage_notifier import cli
from hardware_usage_notifier.cli import exit_codes
from hardware_usage_notifier.cli.options.help import Help

help_option = Help()


@pytest.fixture(scope='function')
def cli_runner():
    return CliRunner()


def test_when_no_argument_then_help_printed(cli_runner):
    no_args_command_result = cli_runner.invoke(cli)
    help_command_result = cli_runner.invoke(cli, [help_option.long_name])

    assert no_args_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert no_args_command_result.output == help_command_result.output


def test_when_short_help_then_same_output_as_long_help(cli_runner):
    short_help_command_result = cli_runner.invoke(cli, [help_option.short_name])
    long_help_command_result = cli_runner.invoke(cli, [help_option.long_name])

    assert short_help_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert long_help_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert short_help_command_result.output == long_help_command_result.output
