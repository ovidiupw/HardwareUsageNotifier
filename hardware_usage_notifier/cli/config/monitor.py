import os

from hardware_usage_notifier.cli.config.interval import Interval
from hardware_usage_notifier.cli.config.metric import Metric
from hardware_usage_notifier.cli.config.threshold import Threshold

from hardware_usage_notifier.cli.config.notifier import Notifier


class Monitor:
    METRICS_DIRECTORY = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'metrics'))
    METRIC_INSTANCES_PARENT_MODULE = 'hardware_usage_notifier.metrics'

    def __init__(self, monitor_config_dict):
        self.name = monitor_config_dict['name']
        self.description = monitor_config_dict.get('description')  # Description is optional, thus we use 'get'
        self.interval = Interval(monitor_config_dict['interval'])
        self.metric = Metric(
            config=monitor_config_dict['metric'],
            metric_directory=Monitor.METRICS_DIRECTORY,
            metric_parent_module=Monitor.METRIC_INSTANCES_PARENT_MODULE)
        self.threshold = Threshold(monitor_config_dict['threshold'])
        self.notifiers = Monitor.Notifiers(monitor_config_dict['notifiers'])

        assert len(self.name) != 0, 'The name of the monitor must contain at least one character!'

    def __eq__(self, other: object) -> bool:
        return self.name == other.name \
               and self.description == other.description \
               and self.interval == other.interval \
               and self.metric == other.metric \
               and self.threshold == other.threshold \
               and self.notifiers == other.notifiers

    def __hash__(self) -> int:
        return hash((self.minutes, self.description, self.interval, self.metric, self.threshold, self.notifiers))

    class Notifiers:
        def __init__(self, notifiers_config_dict):
            self.monitor_alarm = Notifier(notifiers_config_dict['monitor_alarm'])
            self.monitor_failure = Notifier(notifiers_config_dict['monitor_failure'])

        def __eq__(self, other: object) -> bool:
            return self.monitor_alarm == other.monitor_alarm and self.monitor_failure == other.monitor_failure

        def __hash__(self) -> int:
            return hash((self.monitor_alarm, self.monitor_failure))
