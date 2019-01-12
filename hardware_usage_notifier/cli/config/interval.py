class Interval:
    def __init__(self, minutes):
        self.minutes = minutes

        assert self.minutes > 0, f"The interval minutes must be a positive number, but got '{self.minutes}'."

    def __eq__(self, other: object) -> bool:
        return self.minutes == other.minutes

    def __hash__(self) -> int:
        return hash(self.minutes)
