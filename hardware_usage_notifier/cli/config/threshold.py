class Threshold:
    def __init__(self, threshold_config_dict):
        # TODO validation
        self.comparator = threshold_config_dict['comparator']
        self.value = threshold_config_dict['value']
        self.alarm_points = threshold_config_dict['alarm_points']
        self.clear_points = threshold_config_dict['clear_points']


