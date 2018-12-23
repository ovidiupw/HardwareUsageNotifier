from hardware_usage_notifier.cli.config.interval import Interval
from hardware_usage_notifier.util.validators import RunnableExceptionValidator


def test_when_minutes_not_a_positive_number_then_exception():
    exception_validator = RunnableExceptionValidator(lambda: Interval(0))
    exception_validator.verify_exception(
        AssertionError, f"The interval minutes must be a positive number, but got '0'.")


def test_when_minutes_positive_number_then_no_exception():
    Interval(1)
