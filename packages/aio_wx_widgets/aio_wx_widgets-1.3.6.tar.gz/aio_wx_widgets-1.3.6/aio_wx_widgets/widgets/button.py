"""WX button."""

import logging
from asyncio import iscoroutinefunction
from typing import Awaitable, Callable, Union

import wx
from wxasync import AsyncBind  # type: ignore

from aio_wx_widgets.core.base_widget import BaseWidget
from aio_wx_widgets.core.binding import Binding

_LOGGER = logging.getLogger(__name__)

__all__ = ["AioButton"]


class AioButton(BaseWidget):
    """Button widget.

    Args:
        label: button label.
        callback: a coroutine function or normal function. Called when pressed.
    """

    def __init__(
        self,
        label: str,
        callback: Union[
            Callable[[object, wx.Event], Awaitable], Callable[[object, wx.Event], None]
        ],
        enabled: Union[bool, Binding] = True,
        min_width=-1,
    ):
        super().__init__(
            wx.Button(), min_width=min_width, value_binding=None, enabled=enabled
        )
        self._label = label
        self._call_back = callback

    @property
    def label(self):
        """Return the button label."""
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = str(value)
        self.ui_item.SetLabelText(str(self._label))

    def init(self, parent):
        self.ui_item.Create(parent, label=str(self._label))
        if iscoroutinefunction(self._call_back):

            AsyncBind(wx.EVT_BUTTON, self._call_back, self.ui_item)
        else:
            self.ui_item.Bind(wx.EVT_BUTTON, self._call_back)
        self._init()

    def __call__(self, parent):
        self.init(parent)
        # self._make_bindings()
        return self
