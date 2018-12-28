from abc import ABC, abstractmethod


class Metric(ABC):

    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration

    @abstractmethod
    def evaluate(self):
        pass
