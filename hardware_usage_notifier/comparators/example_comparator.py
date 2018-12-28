from hardware_usage_notifier.comparators.comparator import Comparator


class ExampleComparator(Comparator):
    def __init__(self, reference_value):
        super(ExampleComparator, self).__init__(reference_value)

    def compare(self, value):
        pass
