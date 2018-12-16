import os

import jsonschema
import pytest

from hardware_usage_notifier.util.file import read_json_from_file


@pytest.fixture(scope='function')
def json_schema_path():
    return os.path.join(os.path.dirname(__file__),
                        '..', '..', '..', '..', 'hardware_usage_notifier', 'cli', 'config',
                        'config-file-json-schema.json')


def test_when_schema_is_validated_schema_is_itself_valid(json_schema_path):
    json_schema = read_json_from_file(json_schema_path)
    print(os.path.dirname(os.path.realpath(__file__)))
    try:
        jsonschema.validate('', json_schema)
    except jsonschema.exceptions.ValidationError:
        pass  # This test only verifies the jsonschema.exceptions.SchemaError, so we are not interested of any other err
