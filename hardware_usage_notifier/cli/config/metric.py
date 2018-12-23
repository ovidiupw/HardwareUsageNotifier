class Metric:
    def __init__(self, metric_config_dict):
        # TODO validation
        self.name = metric_config_dict['name']
        self.configuration = metric_config_dict.get('configuration')

        assert len(self.name) != 0, 'The name of the metric must contain at least one character!'

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.configuration == other.configuration

    def __hash__(self) -> int:
        return hash((self.name, self.configuration))
