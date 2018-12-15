from hardware_usage_notifier.cli.options.help import Help


class Command:

    def __init__(self, name):
        self.name = name
        self.help = Help()
