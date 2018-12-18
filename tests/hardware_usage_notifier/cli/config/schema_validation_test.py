import os

import jsonschema
import pytest

from hardware_usage_notifier.util.file import read_json_from_file
from hardware_usage_notifier.util.validators import RunnableExceptionValidator

TEST_RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_instances')

EMPTY_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'empty_config.json')
EMPTY_JSON_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'empty_json.json')
EMPTY_MONITORS_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'empty_monitors.json')
UNSPECIFIED_FIELDS_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'unspecified_fields.json')
MONITORS_NOT_ARRAY_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'monitors_not_array.json')
WRONG_MONITOR_TYPE_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'wrong_monitor_type_config.json')
EMPTY_MONITOR_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'empty_monitor_config.json')
NO_MONITOR_METRIC_CONFIG = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_metric_config.json')


@pytest.fixture(scope='function')
def config_json_schema():
    json_schema_path = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', '..', 'hardware_usage_notifier', 'cli', 'config', 'config_file_json_schema.json')
    return read_json_from_file(json_schema_path)


def test_when_schema_is_validated_schema_is_itself_valid(config_json_schema):
    exception_validator = RunnableExceptionValidator(lambda: jsonschema.validate('', config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "'' is not of type 'object'"
    )


def test_when_config_is_empty_json_then_schema_requires_monitors(config_json_schema):
    empty_config = read_json_from_file(EMPTY_JSON_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(empty_config, config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "'monitors' is a required property"
    )


def test_when_config_contains_empty_monitors_then_schema_validates_successfully(config_json_schema):
    empty_monitors_config = read_json_from_file(EMPTY_MONITORS_CONFIG_FILE)
    jsonschema.validate(empty_monitors_config, config_json_schema)


def test_when_config_monitors_is_not_array_then_schema_requires_array(config_json_schema):
    monitors_not_array_config = read_json_from_file(MONITORS_NOT_ARRAY_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(monitors_not_array_config, config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "is not of type 'array'"
    )


def test_when_config_contains_unspecified_fields_then_schema_validates_successfully(config_json_schema):
    unspecified_fields_config = read_json_from_file(UNSPECIFIED_FIELDS_CONFIG_FILE)
    jsonschema.validate(unspecified_fields_config, config_json_schema)


def test_when_config_contains_wrong_monitor_type_then_schema_requires_object_monitor(config_json_schema):
    wrong_monitor_type_config = read_json_from_file(WRONG_MONITOR_TYPE_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(wrong_monitor_type_config, config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "'' is not of type 'object'"
    )


def test_when_config_contains_empty_monitor_then_schema_requires_monitor_name(config_json_schema):
    empty_monitor_config = read_json_from_file(EMPTY_MONITOR_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(empty_monitor_config, config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "'name' is a required property"
    )


def test_when_config_contains_monitor_with_no_metric_then_schema_requires_monitor_metric(config_json_schema):
    no_monitor_metric_config = read_json_from_file(NO_MONITOR_METRIC_CONFIG)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_metric_config, config_json_schema))
    exception_validator.verify_exception_on_function_exec(
        jsonschema.exceptions.ValidationError,
        "'metric' is a required property"
    )
