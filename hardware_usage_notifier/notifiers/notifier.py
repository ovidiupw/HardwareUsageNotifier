from abc import ABC, abstractmethod


class Notifier(ABC):

    def __init__(self, configuration):
        self.configuration = configuration
        super().__init__()

    @abstractmethod
    def notify(self):
        pass
