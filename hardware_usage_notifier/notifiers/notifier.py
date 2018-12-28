from abc import ABC, abstractmethod


class Notifier(ABC):

    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration

    @abstractmethod
    def notify(self):
        pass
