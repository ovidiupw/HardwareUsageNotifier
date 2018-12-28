from abc import ABC, abstractmethod


class Comparator(ABC):

    def __init__(self, reference_value):
        super().__init__()
        self.reference_value = reference_value

    @abstractmethod
    def compare(self, value):
        pass
