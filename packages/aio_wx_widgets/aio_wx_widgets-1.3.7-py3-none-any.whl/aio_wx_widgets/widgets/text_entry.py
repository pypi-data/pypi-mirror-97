"""Text entry widgets."""

# pylint: disable=invalid-name,no-self-use
from __future__ import annotations

import logging
from typing import Any, Callable, Optional, Union

import wx

from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding, TwoWayBindable
from aio_wx_widgets.core.error_message import ErrorPopup
from aio_wx_widgets.core.validators import ValidationError

_LOGGER = logging.getLogger(__name__)

__all__ = ["Entry"]


class Entry(BaseWidget):
    """A general textctrl for any input."""

    def __init__(
        self,
        binding: Binding,
        label: Union[None, int, str] = None,
        validator: Callable[[Any, bool], Any] = None,
        on_change: Callable[[Entry, Any], None] = None,
        min_width=-1,
        enabled: Union[bool, Binding] = True,
    ):
        super().__init__(
            wx.TextCtrl(),
            min_width=min_width,
            value_binding=TwoWayBindable(
                binding,
                self._get_ui_value,
                self._set_ui_value,
                display_error=self.display_error,
            ),
            enabled=enabled,
        )
        self.value: Optional[int] = None
        self._label = label
        self._txt = self.ui_item
        self._validator = validator
        self._popup: Optional[ErrorPopup] = None
        self._allow_none = True

        self.ui_item.Bind(wx.EVT_KILL_FOCUS, self._on_focus_lost)
        self._on_change = on_change

    def _on_focus_lost(self, evt):
        _LOGGER.debug("Lost focus on element.")
        self._value_binding.update_binding(force=True)
        evt.Skip()

    def _set_ui_value(self, value):
        if value is None:
            value = ""
        _LOGGER.debug(
            "Updating text entry with value: %s, instance %s", value, id(self)
        )
        self._txt.SetValue(str(value))
        _LOGGER.debug("Done updating.")

    def _kill_popup(self):
        if self._popup:
            _LOGGER.debug("Destroying popup")
            self._popup.Destroy()
            self._popup = None

    def _get_ui_value(self, force: bool) -> Any:
        self._kill_popup()
        val = self._txt.GetValue()

        if val == "" and self._allow_none:
            assert self._value_binding is not None
            _LOGGER.debug(
                "Setting property to None, %s",
                self._value_binding.binding.bound_property,
            )
            return None

        if self._validator:
            return self._validator(self._txt.GetValue(), force)
        return self._txt.GetValue()

    def _on_ui_change(self, *args, **kwargs):
        self._value_binding.on_ui_change(*args, **kwargs)

        if self._on_change:
            self._on_change(self, self._get_ui_value(True))

    def init(self, parent):
        args = dict({"parent": parent})
        if self._label:
            args["value"] = str(self._label)

        self._txt.Create(**args)
        # self.ui_item.SetSizeHints(self._min_width, -1)
        self._txt.Bind(wx.EVT_TEXT, self._on_ui_change)

        # self._make_bindings()
        self._init()

    def __call__(self, parent):
        self.init(parent)
        return self

    def display_error(self, exception: ValidationError):
        """Display a validation error."""
        self._kill_popup()

        message = str(exception)
        self._popup = ErrorPopup(self.ui_item, message, style=wx.SIMPLE_BORDER)

        pos = self.ui_item.ClientToScreen((0, 0))
        sz = self.ui_item.GetSize()
        self._popup.Position(pos, (0, sz[1]))
        self._popup.Show()
        self.ui_item.SetFocus()
