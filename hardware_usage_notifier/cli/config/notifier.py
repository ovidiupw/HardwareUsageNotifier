class Notifier:
    def __init__(self, notifier_config_dict):
        # TODO validation
        self.name = notifier_config_dict['name']
        self.configuration = notifier_config_dict['configuration']

        assert len(self.name) != 0, 'The name of the notifier must contain at least one character!'

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.configuration == other.configuration

    def __hash__(self) -> int:
        return hash((self.name, self.configuration))
