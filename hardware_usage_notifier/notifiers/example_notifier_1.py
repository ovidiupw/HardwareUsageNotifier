from hardware_usage_notifier.notifiers.notifier import Notifier


class ExampleNotifier1(Notifier):
    def __init__(self, configuration):
        super(ExampleNotifier1, self).__init__(configuration)

    def notify(self):
        pass
