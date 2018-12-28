from hardware_usage_notifier.metrics.metric import Metric


class NoopMetric(Metric):
    def __init__(self, configuration):
        super().__init__(configuration)

    def evaluate(self):
        pass
