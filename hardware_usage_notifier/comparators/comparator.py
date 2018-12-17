from abc import ABC, abstractmethod


class Comparator(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def compare(self, value, reference):
        pass
