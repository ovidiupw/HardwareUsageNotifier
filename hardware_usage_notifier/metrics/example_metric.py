from hardware_usage_notifier.metrics.metric import Metric


class Example(Metric):
    def __init__(self, configuration):
        super(Example, self).__init__(configuration)

    def evaluate(self):
        pass
