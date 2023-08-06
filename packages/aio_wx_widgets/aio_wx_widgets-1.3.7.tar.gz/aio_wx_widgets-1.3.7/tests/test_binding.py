import logging
from unittest.mock import Mock

import pytest

from aio_wx_widgets.controller import BaseController
from aio_wx_widgets.core.binding import WATCHERS, Binding, TwoWayBindable

_LOGGER = logging.getLogger(__name__)
#
# class SomeBinding(Binding):
#


class SomeController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.a_value = 10


@pytest.fixture
def some_controller(base_model):
    return SomeController(base_model)


@pytest.fixture
def some_binding(some_controller):
    return Binding(bound_object=some_controller, bound_property="a_value")


@pytest.fixture
def some_bindable(mocker, some_binding):
    get_ui_value = Mock()
    set_ui_value = Mock()
    # mocker.patch.object(TwoWayBindable, "_get_ui_value")
    # mocker.patch.object(TwoWayBindable, "_set_ui_value")

    return TwoWayBindable(some_binding, get_ui_value, set_ui_value)


def test_make_binding(some_bindable, some_controller):
    some_bindable.make_binding()

    # check if watcher is added to list of watchers.
    watchers = some_controller.__dict__[WATCHERS]["a_value"]
    assert len(watchers) == 1

    # Check if widget is updated with the default value.
    some_bindable._set_ui_value.assert_called_once_with(10)
