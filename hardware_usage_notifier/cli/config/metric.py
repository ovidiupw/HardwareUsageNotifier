class Metric:
    def __init__(self, metric_config_dict):
        # TODO validation
        self.name = metric_config_dict['name']
        self.configuration = metric_config_dict['configuration']
