import logging

import pytest

from aio_wx_widgets.core.validators import (
    ValidationError,
    all_digits_validator,
    int_validator,
)

_LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("incoming,expected", [("0", 0), ("1", 1), ("-1", -1)])
def test_int_validator(incoming, expected):

    result = int_validator(incoming, True)

    assert isinstance(result, int)
    assert result == expected


@pytest.mark.parametrize("incoming", ["a"])
def test_int_validator_fail(incoming):
    with pytest.raises(ValidationError):
        int_validator(incoming, True)


@pytest.mark.parametrize("incoming", ["0002340324"])
def test_all_digits_validator(incoming):
    result = all_digits_validator(incoming, True)

    assert result == incoming


@pytest.mark.parametrize("incoming", ["000234a0324"])
def test_all_digits_validator_fail(incoming):
    with pytest.raises(ValidationError):
        all_digits_validator(incoming, True)
