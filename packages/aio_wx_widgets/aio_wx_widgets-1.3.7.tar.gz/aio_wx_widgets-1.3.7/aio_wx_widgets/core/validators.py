"""Validators"""

import logging
from typing import Union

_LOGGER = logging.getLogger(__name__)

__all__ = [
    "int_validator",
    "float_validator",
    "all_digits_validator",
    "ValidationError",
]


def int_validator(value, force) -> int:  # noqa
    """Int validator."""
    try:
        converted = int(value)
    except ValueError:
        raise ValidationError("Not a valid integer.") from None
    if value == str(converted):
        return converted
    raise ValidationError("not a valid integer.")


def float_validator(value: str, force) -> Union[float, str]:
    """Float validator."""
    try:
        converted = float(value)
    except ValueError:
        raise ValidationError("Not a valid float.") from None
    if value == str(converted):
        return converted
    if force:
        return converted
    return value


def all_digits_validator(value: str, force) -> str:  # noqa
    """All digits validator.

    Only numbers are allowed.
    """
    if value.isdigit():
        return value
    raise ValidationError("Only numbers are allowed.")


class ValidationError(Exception):
    """Input validation error"""
