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
NO_MONITOR_METRIC_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_metric_config.json')
NO_MONITOR_THRESHOLD_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_threshold_config.json')
NO_MONITOR_INTERVAL_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_interval_config.json')
NO_MONITOR_NOTIFIERS_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_notifiers_config.json')
NO_METRIC_NAME_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_metric_name_config.json')
NO_METRIC_CONFIGURATION_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_metric_configuration_config.json')
NO_THRESHOLD_COMPARATOR_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_threshold_comparator_config.json')
NO_THRESHOLD_VALUE_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_threshold_value_config.json')
NO_THRESHOLD_ALARM_POINTS_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_threshold_alarm_points_config.json')
NO_THRESHOLD_CLEAR_POINTS_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_threshold_clear_points_config.json')
NO_NOTIFIERS_MONITOR_ALARM_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_notifiers_monitor_alarm_config.json')
NO_NOTIFIERS_MONITOR_FAILURE_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_notifiers_monitor_failure_config.json')
NO_MONITOR_ALARM_NAME_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_alarm_name_config.json')
NO_MONITOR_ALARM_CONFIGURATION_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_alarm_configuration_config.json')
NO_MONITOR_FAILURE_NAME_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_failure_name_config.json')
NO_MONITOR_FAILURE_CONFIGURATION_CONFIG_FILE = os.path.join(TEST_RESOURCES_DIRECTORY, 'no_monitor_failure_configuration_config.json')


@pytest.fixture(scope='function')
def config_json_schema():
    json_schema_path = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', '..', 'hardware_usage_notifier', 'cli', 'config', 'config_file_json_schema.json')
    return read_json_from_file(json_schema_path)


def test_when_schema_is_validated_schema_is_itself_valid(config_json_schema):
    exception_validator = RunnableExceptionValidator(lambda: jsonschema.validate('', config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'' is not of type 'object'",
        []
    )


def test_when_config_is_empty_json_then_schema_requires_monitors(config_json_schema):
    empty_config = read_json_from_file(EMPTY_JSON_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(empty_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'monitors' is a required property",
        []
    )


def test_when_config_contains_empty_monitors_then_schema_validates_successfully(config_json_schema):
    empty_monitors_config = read_json_from_file(EMPTY_MONITORS_CONFIG_FILE)
    jsonschema.validate(empty_monitors_config, config_json_schema)


def test_when_config_monitors_is_not_array_then_schema_requires_array(config_json_schema):
    monitors_not_array_config = read_json_from_file(MONITORS_NOT_ARRAY_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(monitors_not_array_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "is not of type 'array'",
        ['monitors']
    )


def test_when_config_contains_unspecified_fields_then_schema_validates_successfully(config_json_schema):
    unspecified_fields_config = read_json_from_file(UNSPECIFIED_FIELDS_CONFIG_FILE)
    jsonschema.validate(unspecified_fields_config, config_json_schema)


def test_when_config_contains_wrong_monitor_type_then_schema_requires_object_monitor(config_json_schema):
    wrong_monitor_type_config = read_json_from_file(WRONG_MONITOR_TYPE_CONFIG_FILE)
    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(wrong_monitor_type_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'' is not of type 'object'",
        ['monitors', 0]
    )


def test_when_config_contains_empty_monitor_then_schema_requires_monitor_name(config_json_schema):
    empty_monitor_config = read_json_from_file(EMPTY_MONITOR_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(empty_monitor_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'name' is a required property",
        ['monitors', 0]
    )


def test_when_config_contains_monitor_with_no_metric_then_schema_requires_monitor_metric(config_json_schema):
    no_monitor_metric_config = read_json_from_file(NO_MONITOR_METRIC_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_metric_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'metric' is a required property",
        ['monitors', 0]
    )


def test_when_config_contains_monitor_with_no_threshold_then_schema_requires_monitor_threshold(config_json_schema):
    no_monitor_threshold_config = read_json_from_file(NO_MONITOR_THRESHOLD_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_threshold_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'threshold' is a required property",
        ['monitors', 0]
    )


def test_when_config_contains_monitor_with_no_interval_then_schema_requires_monitor_interval(config_json_schema):
    no_monitor_interval_config = read_json_from_file(NO_MONITOR_INTERVAL_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_interval_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'interval' is a required property",
        ['monitors', 0]
    )


def test_when_config_contains_monitor_with_no_notifiers_then_schema_requires_monitor_notifiers(config_json_schema):
    no_monitor_notifiers_config = read_json_from_file(NO_MONITOR_NOTIFIERS_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_notifiers_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'notifiers' is a required property",
        ['monitors', 0]
    )


def test_when_config_contains_metric_with_no_name_then_schema_requires_metric_name(config_json_schema):
    no_metric_name_config = read_json_from_file(NO_METRIC_NAME_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_metric_name_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'name' is a required property",
        ['monitors', 0, 'metric']
    )


def test_when_config_contains_metric_with_no_configuration_then_schema_validates_successfully(config_json_schema):
    no_metric_configuration_config = read_json_from_file(NO_METRIC_CONFIGURATION_CONFIG_FILE)
    jsonschema.validate(no_metric_configuration_config, config_json_schema)


def test_when_config_contains_threshold_with_no_comparator_then_schema_requires_comparator(config_json_schema):
    no_threshold_comparator_config = read_json_from_file(NO_THRESHOLD_COMPARATOR_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_threshold_comparator_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'comparator' is a required property",
        ['monitors', 0, 'threshold']
    )


def test_when_config_contains_threshold_with_no_value_then_schema_requires_value(config_json_schema):
    no_threshold_value_config = read_json_from_file(NO_THRESHOLD_VALUE_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_threshold_value_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'value' is a required property",
        ['monitors', 0, 'threshold']
    )


def test_when_config_contains_threshold_with_no_clear_points_then_schema_requires_clear_points(config_json_schema):
    no_threshold_clear_points_config = read_json_from_file(NO_THRESHOLD_CLEAR_POINTS_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_threshold_clear_points_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'clear_points' is a required property",
        ['monitors', 0, 'threshold']
    )


def test_when_config_contains_notifiers_with_no_monitor_alarm_then_schema_validates_successfully(config_json_schema):
    no_notifiers_monitor_alarm_config = read_json_from_file(NO_NOTIFIERS_MONITOR_ALARM_CONFIG_FILE)
    jsonschema.validate(no_notifiers_monitor_alarm_config, config_json_schema)


def test_when_config_contains_notifiers_with_no_monitor_failure_then_schema_validates_successfully(config_json_schema):
    no_notifiers_monitor_failure_config = read_json_from_file(NO_NOTIFIERS_MONITOR_FAILURE_CONFIG_FILE)
    jsonschema.validate(no_notifiers_monitor_failure_config, config_json_schema)


def test_when_config_contains_monitor_alarm_with_no_name_then_schema_requires_name(config_json_schema):
    no_monitor_alarm_name_config = read_json_from_file(NO_MONITOR_ALARM_NAME_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_alarm_name_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'name' is a required property",
        ['monitors', 0, 'notifiers', 'monitor_alarm']
    )


def test_when_config_contains_monitor_alarm_with_no_configuration_then_schema_validates_successfully(config_json_schema):
    no_monitor_alarm_configuration_config = read_json_from_file(NO_MONITOR_ALARM_CONFIGURATION_CONFIG_FILE)
    jsonschema.validate(no_monitor_alarm_configuration_config, config_json_schema)


def test_when_config_contains_monitor_failure_with_no_name_then_schema_requires_name(config_json_schema):
    no_monitor_failure_name_config = read_json_from_file(NO_MONITOR_FAILURE_NAME_CONFIG_FILE)

    exception_validator = RunnableExceptionValidator(
        lambda: jsonschema.validate(no_monitor_failure_name_config, config_json_schema))
    exception_validator.verify_json_schema_exception(
        jsonschema.exceptions.ValidationError,
        "'name' is a required property",
        ['monitors', 0, 'notifiers', 'monitor_failure']
    )


def test_when_config_contains_monitor_failure_with_no_configuration_then_schema_validates_successfully(config_json_schema):
    no_monitor_failure_configuration_config = read_json_from_file(NO_MONITOR_FAILURE_CONFIGURATION_CONFIG_FILE)
    jsonschema.validate(no_monitor_failure_configuration_config, config_json_schema)
