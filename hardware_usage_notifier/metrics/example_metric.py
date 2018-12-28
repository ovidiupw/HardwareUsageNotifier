from hardware_usage_notifier.metrics.metric import Metric


class ExampleMetric(Metric):
    def __init__(self, configuration):
        super(ExampleMetric, self).__init__(configuration)

    def evaluate(self):
        pass
