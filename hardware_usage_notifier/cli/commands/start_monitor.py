from hardware_usage_notifier.cli.config.config import Config
from hardware_usage_notifier.cli.commands.command import Command
from hardware_usage_notifier.cli.options.config_file import ConfigFile


class StartMonitor(Command):

    def __init__(self, click, jsonschema):
        config = Config(click=click, jsonschema=jsonschema)
        Command.__init__(self, name='start-monitor')
        self.config_file = ConfigFile(config)
