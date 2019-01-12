from hardware_usage_notifier.notifiers.notifier import Notifier


class NoopNotifier(Notifier):
    def __init__(self, configuration):
        super().__init__(configuration)

    def notify(self):
        pass
