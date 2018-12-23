class Threshold:
    def __init__(self, threshold_config_dict):
        # TODO validation
        self.comparator = threshold_config_dict['comparator']
        self.value = threshold_config_dict['value']
        self.alarm_points = int(threshold_config_dict['alarm_points'])
        self.clear_points = int(threshold_config_dict['clear_points'])

        assert len(self.comparator) != 0, 'The threshold comparator must contain at least one character!'
        assert self.alarm_points > 0, \
            f"The threshold alarm points must be a positive integer, but got '{self.alarm_points}'!"
        assert self.clear_points > 0, \
            f"The threshold clear points must be a positive integer, but got '{self.clear_points}'!"

    def __eq__(self, other: object) -> bool:
        return self.comparator == other.comparator \
               and self.value == other.value \
               and self.alarm_points == other.alarm_points \
               and self.clear_points == other.clear_points

    def __hash__(self) -> int:
        return hash((self.comparator, self.value, self.alarm_points, self.clear_points))
