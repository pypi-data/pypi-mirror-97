"""Base widget"""

from __future__ import annotations

import logging
from typing import Generic, TypeVar, Union

from aio_wx_widgets.core.binding import Binding, OneWayBindable, TwoWayBindable

_LOGGER = logging.getLogger(__name__)

WxItem = TypeVar("WxItem")


class CallableItem:
    """An item that is callable. (Able to be added to a container)."""

    def init(self, parent):
        """Initialize this aio-item"""
        raise NotImplementedError()

    @property
    def ui_item(self):
        """A wxPython element."""
        raise NotImplementedError()


class BaseWidget(CallableItem, Generic[WxItem]):
    """All widgets should inherit from this."""

    def __init__(
        self,
        ui_item: WxItem,
        min_width: int,
        value_binding: Union[OneWayBindable, TwoWayBindable, None],
        enabled: Union[bool, Binding] = True,
    ):
        self._enabled = enabled
        self._ui_item = ui_item
        self._value_binding = value_binding
        self._min_width = min_width

        self._enabled_binding = None
        if isinstance(self._enabled, Binding):
            self._enabled_binding = OneWayBindable(
                self._enabled, self._set_enabled_value
            )

    @property
    def ui_item(self) -> WxItem:
        return self._ui_item

    def _set_enabled_value(self, enabled):
        if enabled:
            self.ui_item.Enable()
        else:
            self.ui_item.Disable()

    def _make_bindings(self):
        if self._value_binding:
            self._value_binding.make_binding()
        if self._enabled_binding:
            self._enabled_binding.make_binding()

    def _init(self):
        self._make_bindings()
        if self._min_width > -1:
            actual_x_value = self.ui_item.GetSize()[0]
            if actual_x_value < self._min_width:
                self.ui_item.SetMinSize((self._min_width, -1))

    def init(self, parent):
        raise NotImplementedError()

    def __call__(self, parent):
        raise NotImplementedError()
