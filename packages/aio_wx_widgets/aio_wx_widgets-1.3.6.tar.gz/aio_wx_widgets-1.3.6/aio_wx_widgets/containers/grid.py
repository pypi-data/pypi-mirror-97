"""Grid layout item."""

# pylint: disable=duplicate-code

from __future__ import annotations

import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem
from aio_wx_widgets.core.sizers import SizerMixin

_LOGGER = logging.getLogger(__name__)

__all__ = ["Grid", "VERTICAL", "HORIZONTAL"]

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL


class Grid(SizerMixin, CallableItem):
    """A grid component.

    Basically a boxsizer with some defaults.
    """

    default_sizer_margin = 0

    HOR = HORIZONTAL
    VER = VERTICAL

    def __init__(self, orientation=HORIZONTAL):
        """Init."""
        super().__init__()
        self._sizer_ = wx.BoxSizer(orient=orientation)
        self._parent = None

    @property
    def ui_item(self):
        """Return UI item."""
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        # setting a specific parent.
        self.init(parent)
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
