from hardware_usage_notifier.cli.options.option import Option


class Help(Option):

    def __init__(self):
        Option.__init__(self,
                        short_name='-h',
                        long_name='--help')
