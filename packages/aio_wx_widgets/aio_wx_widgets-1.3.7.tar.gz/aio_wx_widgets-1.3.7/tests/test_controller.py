import logging
from unittest.mock import Mock

from aio_wx_widgets.core.binding import WATCHERS

_LOGGER = logging.getLogger(__name__)


def test_set_attr_no_watcher(base_controller):
    """Smoke test.

    Check whether setting an attribute "just" works.
    """
    base_controller.a_value = 10

    assert base_controller.a_value == 10


def test_set_attr_watcher_no_subscription(base_controller):
    base_controller.__dict__[WATCHERS] = {}

    base_controller.a_value = 10

    assert base_controller.a_value == 10
    assert "a_value" not in base_controller.__dict__[WATCHERS]


def test_set_attr_watcher_watched(base_controller):
    base_controller.__dict__[WATCHERS] = {}
    mock_watcher = Mock()
    base_controller.__dict__[WATCHERS]["a_value"] = [mock_watcher]

    base_controller.a_value = 10

    mock_watcher.assert_called_with(10)
