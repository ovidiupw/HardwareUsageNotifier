from hardware_usage_notifier.comparators.comparator import Comparator


class NoopComparator(Comparator):
    def __init__(self, reference_value):
        super().__init__(reference_value)

    def compare(self, value):
        pass
