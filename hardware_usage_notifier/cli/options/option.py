class Option:

    def __init__(self, short_name, long_name, option_type=None, required=False, default='', callback=None):
        self.short_name = short_name
        self.long_name = long_name
        self.type = option_type
        self.required = required
        self.default = default
        self.callback = callback
