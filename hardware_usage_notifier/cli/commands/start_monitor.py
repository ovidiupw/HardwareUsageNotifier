from hardware_usage_notifier.cli.commands.command import Command
from hardware_usage_notifier.cli.options.config_file import ConfigFile


class StartMonitor(Command):

    def __init__(self):
        Command.__init__(self, name='start-monitor')
        self.config_file = ConfigFile()



