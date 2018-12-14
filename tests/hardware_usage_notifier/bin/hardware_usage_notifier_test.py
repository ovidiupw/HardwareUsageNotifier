# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner
from hardware_usage_notifier.bin import hardware_usage_notifier
from hardware_usage_notifier.common import exit_codes


@pytest.fixture(scope='function')
def cli_runner():
    return CliRunner()


def test_when_no_argument_then_help_printed(cli_runner):
    no_args_command_result = cli_runner.invoke(hardware_usage_notifier.cli)
    help_command_result = cli_runner.invoke(hardware_usage_notifier.cli, ['--help'])

    assert no_args_command_result.exit_code == 0
    assert no_args_command_result.exit_code == exit_codes.SUCCESS_EXIT_CODE
    assert no_args_command_result.output == help_command_result.output




