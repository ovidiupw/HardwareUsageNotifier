from click import STRING

from hardware_usage_notifier.cli.options.option import Option
from hardware_usage_notifier.cli.config.config import Config


class ConfigFile(Option):

    def __init__(self):
        Option.__init__(self,
                        short_name='-c',
                        long_name='--config-file',
                        required=True,
                        option_type=STRING,
                        default='hun-config.json',
                        callback=Config.from_cli_file_path_param)
