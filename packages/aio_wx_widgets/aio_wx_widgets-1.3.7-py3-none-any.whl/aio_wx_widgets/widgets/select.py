"""A dropdown selection widget."""

from __future__ import annotations

import logging
from typing import Callable, Optional, Sequence, Union

import wx

from aio_wx_widgets import type_annotations as T  # noqa
from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding, TwoWayBindable

_LOGGER = logging.getLogger(__name__)

__all__ = ["Select"]


class Select(BaseWidget):
    """Dropdown selection widget."""

    def __init__(
        self,
        choices: Sequence[T.Choice],
        on_select_callback: Optional[Callable[[T.Choice], None]] = None,
        binding: Optional[T.Binding] = None,
        min_width=300,
        enabled: Union[bool, Binding] = True,
    ):
        """
        Init.

        Args:
            choices: A sequence of Choice objects.
                A choice object must have a label property which is displayed in the
                pull down and a value property which is returned when the selection
                is made.
            on_select_callback: called when selection is made.
            binding: A property bound to a selected Choice object.
            min_width: when alignment is set, this is the advised minimal width the
                the widget should take.
        """
        value_binding = (
            TwoWayBindable(binding, self._get_ui_value, self._set_ui_value)
            if binding is not None
            else None
        )

        super().__init__(
            wx.Choice(), min_width, value_binding=value_binding, enabled=enabled,
        )
        self.choices = choices
        self._on_select_callback = on_select_callback
        self._selected_item = None

        self.ui_item.Bind(wx.EVT_CHOICE, self._on_choice)
        self.ui_item.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)
        self._min_width = min_width

    def _on_mouse_wheel(self, evt):
        """Capturing as I want to disable selection when scrolling"""

    def _set_ui_value(self, value: Optional[T.Choice]):
        if value is not None:
            try:
                _idx = next(
                    (
                        i
                        for i, val in enumerate(self.choices)
                        if val.value == value.value
                    )
                )
            except StopIteration:
                _LOGGER.error("Default product not available")
            else:
                self.ui_item.Select(_idx)
        # setting this value manually as the SetValue command does -in this case-
        # not trigger the _on_ui_change callback.
        assert self._value_binding is not None
        self._value_binding.fire_update_event = True

    def _on_choice(self, event):  # noqa
        _idx = self.ui_item.GetSelection()
        _LOGGER.debug("Selected idx: %s", _idx)
        self._selected_item = self.choices[_idx]
        if self._value_binding:
            self._value_binding.on_ui_change()
        if self._on_select_callback:
            self._on_select_callback(self._selected_item)

    def _get_ui_value(self, force):  # noqa
        return self._selected_item

    def init(self, parent):
        self.ui_item.Create(parent, choices=[choice.label for choice in self.choices])
        self._init()

    def __call__(self, parent):
        self.init(parent)
        return self
