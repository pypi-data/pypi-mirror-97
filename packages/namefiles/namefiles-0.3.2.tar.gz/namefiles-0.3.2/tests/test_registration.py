from namefiles import register_filename_validator
import pytest


def test_register_exceptions():
    sample_naming_convention = {}
    with pytest.raises(TypeError):
        register_filename_validator({})

    with pytest.raises(KeyError):
        from jsonschema import Draft7Validator
        register_filename_validator(Draft7Validator({}))

    test_convention = {
        "name": "test_convention",
    }
    assert register_filename_validator(Draft7Validator(test_convention))