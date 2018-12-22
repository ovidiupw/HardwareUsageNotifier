class Notifier:
    def __init__(self, notifier_config_dict):
        # TODO validation
        self.name = notifier_config_dict['name']
        self.configuration = notifier_config_dict['configuration']
