import click

from hardware_usage_notifier.cli.options.option import Option


class ConfigFile(Option):

    def __init__(self, config):
        Option.__init__(self,
                        short_name='-c',
                        long_name='--config-file',
                        required=True,
                        option_type=click.STRING,
                        default='hun-config.json',
                        callback=config.from_cli_file_path_param)
