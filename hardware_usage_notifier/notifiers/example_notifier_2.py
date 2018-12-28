from hardware_usage_notifier.notifiers.notifier import Notifier


class ExampleNotifier2(Notifier):
    def __init__(self, configuration):
        super(ExampleNotifier2, self).__init__(configuration)

    def notify(self):
        pass
