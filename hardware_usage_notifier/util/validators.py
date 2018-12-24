import os

from hardware_usage_notifier.util.string import string_contains
from hardware_usage_notifier.util.file import list_classes_in_file

class RunnableExceptionValidator:
    def __init__(self, function):
        self.function = function

    def verify_json_schema_exception(self, exception, message_substring, absolute_path):
        try:
            self.function()
        except exception as e:
            assert string_contains(e.args[0],
                                   message_substring), f"Expected exception message to contain string '{message_substring}', but got '{e.args[0]}'!"
            assert list(
                e.absolute_path) == absolute_path, f"Expected exception to have occurred at object path '{absolute_path}', but got exception at object path '{e.absolute_path}'!"
            return
        raise Exception(
            f"Expected function to raise exception of type '{exception.__name__}', but function did not raise exception!")

    def verify_exception(self, exception, message_substring):
        try:
            self.function()
        except exception as e:
            assert string_contains(e.args[0],
                                   message_substring), f"Expected exception message to contain string '{message_substring}', but got '{e.args[0]}'!"
            return
        raise Exception(
            f"Expected function to raise exception of type '{exception.__name__}', but function did not raise exception!")


class FileValidator:
    @staticmethod
    def is_file_path_valid(file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    @staticmethod
    def does_file_contains_single_class(file_path):
        return len(list_classes_in_file(file_path)) == 1
