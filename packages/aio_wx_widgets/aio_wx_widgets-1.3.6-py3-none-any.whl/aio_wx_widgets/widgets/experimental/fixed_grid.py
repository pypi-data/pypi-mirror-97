"""A fixed grid.

when resizing windows this layout seems to be most reliable.
"""

from __future__ import annotations

import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem

_LOGGER = logging.getLogger(__name__)


class FixedGrid(CallableItem):
    """A fixed grid implementation.

    When resizing windows this grid behaves best.
    """
    def __init__(self):
        self._sizer_ = wx.GridSizer(1, 0, (0, 0))
        self._parent = None

    @property
    def ui_item(self):
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self) -> FixedGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""

    def _check_columns(self):
        used_cols = self._sizer_.GetEffectiveColsCount()
        _LOGGER.debug("Used cols %s", used_cols)
        total_cols = self._sizer_.GetCols()
        if total_cols == used_cols:
            self._sizer_.SetCols(used_cols + 1)

    def add(self, item, create=True):
        """Add an item to this grid."""
        self._check_columns()
        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        self._sizer_.Add(item.ui_item, 1, wx.EXPAND)
        return item

    def add_spacer(self):
        """Add an empty space to a column."""
        self._check_columns()
        self._sizer_.Add(wx.Panel(self._parent),1,flag=wx.EXPAND)


class DynamicGrid(CallableItem):
    """A dynamic grid. Allows for column spanning etc."""
    def __init__(self):
        self._sizer_ = wx.GridBagSizer()
        self._sizer_.SetFlexibleDirection(wx.VERTICAL)
        self._sizer_.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        self._parent = None

    @property
    def ui_item(self):
        return self._sizer_

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self) -> DynamicGrid:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""

    def add(self, item, col, span=1, create=True):
        """Add an item to this grid."""

        if create:
            assert isinstance(item, CallableItem)
            item.init(self._parent)

        self._sizer_.Add(item.ui_item, (0, col), (1, span), flag=wx.EXPAND)
        self._set_col_sizes_equal()
        return item

    def _set_col_sizes_equal(self):
        for idx in range(self._sizer_.Cols):
            if not self._sizer_.IsColGrowable(idx):
                self._sizer_.AddGrowableCol(idx)


    def add_spacer(self,col,span=1):
        """Add an empty space to a column and/or span."""
        self._sizer_.Add(wx.Panel(self._parent),(0,col),(1,span),flag=wx.EXPAND)
        self._set_col_sizes_equal()
