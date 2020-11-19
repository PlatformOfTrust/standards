"""This module has functions used for validations."""
from typing import Sequence

from utils.constants import CLASS, PROPERTY, _TYPE

from validators.validator import Validator


def call_validators(validators: Sequence[Validator], stop: bool = False)\
        -> bool:
    """This function calls the validate method for all validators from
    validators parameter and returns True if all validations pass and False
    otherwise."""

    valid = True
    for validator in validators:
        valid &= validator.validate()

        if stop and not valid:
            return False

    return valid


def is_class(item: dict) -> bool:
    """This function checks if an object is of type Class."""

    if _TYPE not in item:
        return False

    if item[_TYPE].endswith(CLASS):
        return True

    return False


def is_property(item: dict) -> bool:
    """This function checks if an object is of type Property."""

    if _TYPE not in item:
        return False

    if item[_TYPE].endswith(PROPERTY) or\
            item[_TYPE] == "dli:SupportedAttribute":
        return True

    return False
