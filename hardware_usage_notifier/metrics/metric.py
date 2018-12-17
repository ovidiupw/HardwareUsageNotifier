from abc import ABC, abstractmethod


class Metric(ABC):

    def __init__(self, configuration):
        self.configuration = configuration
        super().__init__()

    @abstractmethod
    def evaluate(self):
        pass
