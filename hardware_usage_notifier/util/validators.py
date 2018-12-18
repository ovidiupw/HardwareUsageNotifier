from hardware_usage_notifier.util.string import string_contains


class RunnableExceptionValidator:
    def __init__(self, function):
        self.function = function

    def verify_exception_on_function_exec(self, exception, message_substring):
        try:
            self.function()
        except exception as e:
            assert string_contains(e.message, message_substring)
            return
        raise Exception(
            f"Expected function to raise exception containing message '{message_substring}', but function did not raise exception!")
