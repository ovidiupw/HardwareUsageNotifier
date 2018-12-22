from hardware_usage_notifier.cli.config.interval import Interval
from hardware_usage_notifier.cli.config.metric import Metric
from hardware_usage_notifier.cli.config.threshold import Threshold

from hardware_usage_notifier.cli.config.notifier import Notifier


class Monitor:

    def __init__(self, monitor_config_dict):
        self.name = monitor_config_dict['name']
        self.description = monitor_config_dict.get('description')  # Description is optional, thus we use 'get'
        self.interval = Interval(monitor_config_dict['interval'])
        self.metric = Metric(monitor_config_dict['metric'])
        self.threshold = Threshold(monitor_config_dict['threshold'])
        self.notifiers = Monitor.Notifiers(monitor_config_dict['notifiers'])

        assert len(self.name) != 0, 'The name of the monitor must contain at least one character!'

    class Notifiers:
        def __init__(self, notifiers_config_dict):
            self.monitor_alarm = Notifier(notifiers_config_dict['monitor_alarm'])
            self.monitor_failure = Notifier(notifiers_config_dict['monitor_failure'])
