"""Checkbox."""

import logging
from typing import Callable, Optional, Union

import wx

from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding, TwoWayBindable

_LOGGER = logging.getLogger(__name__)

__all__ = ["CheckBox"]


class CheckBox(BaseWidget):
    """Checkbox widget."""

    def __init__(
        self,
        label: str,
        binding: Optional[Binding],
        change_callback: Optional[Callable[[bool], None]] = None,
        enabled: Union[bool, Binding] = True,
        min_width=-1,
    ):
        """Init.

        Args:
            label: Checkbox label
            binding: property binding.
            change_callback: called when checkbox value changes.
        """

        value_binding = (
            TwoWayBindable(binding, self._get_ui_value, self._set_ui_value)
            if binding is not None
            else None
        )
        super().__init__(
            wx.CheckBox(),
            min_width=min_width,
            value_binding=value_binding,
            enabled=enabled,
        )
        self._label = label
        self._change_callback = change_callback

    def _set_ui_value(self, value):
        val = bool(value)
        _LOGGER.debug("Setting value to %s, %s", val, id(self))
        self.ui_item.SetValue(val)

        # setting this value manually as the SetValue command does -in this case-
        # not trigger the _on_ui_change callback.
        self._value_binding.fire_update_event = True

    def _get_ui_value(self, force: bool) -> bool:  # noqa
        val: bool = self.ui_item.GetValue()
        return val

    def _on_ui_change(self, *args, **kwargs):
        self._value_binding.on_ui_change(*args, **kwargs)

        if self._change_callback:
            self._change_callback(self._get_ui_value(True))

    def init(self, parent):
        self.ui_item.Create(parent, label=str(self._label))
        self.ui_item.Bind(wx.EVT_CHECKBOX, self._on_ui_change)
        self._init()

    def __call__(self, parent):
        _LOGGER.warning("__call__ will be removed in the future. Use `init` instead")
        self.init(parent)

        return self
