"""Group layout item. Draws a line around children and sets a title."""


import logging

import wx

from aio_wx_widgets.core.base_widget import CallableItem
from aio_wx_widgets.core.sizers import SizerMixin
from aio_wx_widgets.widgets import text

_LOGGER = logging.getLogger(__name__)

__all__ = ["Group", "Section"]


class Group(SizerMixin, CallableItem):
    """A Group widget.

    +--<LABEL>-------------+
    |                      |
    |  - Widget 1          |
    |  - Widget 2          |
    |                      |
    +----------------------+

    """

    default_sizer_margin = 20

    def __init__(self, label, **kwargs):
        """Init.

        Args:
            label:
        """
        super().__init__()
        self._label = label
        self._extra_bottom_border = 10
        self._sizer_ = wx.BoxSizer(wx.VERTICAL)
        self._ui_item = wx.StaticBox()
        # kwargs["sizer"] = self._sizer
        self._bottom_border = 1
        # self._ui_item.SetSizer(self._sizer_)

    @property
    def _sizer(self):
        return self._sizer_

    @property
    def ui_item(self):
        """Return UI item."""
        return self._ui_item

    def init(self, parent):
        """Call this class as a function.

        Args:
            parent: The parent of this ui item.

        """
        self.ui_item.Create(parent, label=self._label)

        top, other = self.ui_item.GetBordersForSizer()
        self._bottom_border = other + self._extra_bottom_border
        self._sizer.AddSpacer(top + 5)
        self.ui_item.SetSizer(self._sizer)

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        self._finish()

    def _finish(self):
        self._sizer.AddSpacer(self._bottom_border)


class Section(SizerMixin, CallableItem):
    """A section with a large header text and an optional closing line.

    LARGE HEADER TEXT

    - content
    - content
    ----------------------------------- [optional closing line]
    """

    def __init__(self, header: str, add_closing_line=True):
        """Init."""
        super().__init__()
        self._ui_item = self._sizer_ = wx.BoxSizer(orient=wx.VERTICAL)
        self._parent = None
        self._header = header
        self._add_closing_line = add_closing_line

    @property
    def ui_item(self):
        """Return UI item."""
        return self._ui_item

    @property
    def _sizer(self):
        return self._sizer_

    def init(self, parent):
        self._parent = parent

    def __call__(self, parent):
        self.init(parent)
        return self

    def __enter__(self):
        """Enter the context manager."""
        self.add(
            text.Text(text=self._header, font_size=1.5, bold=True), margin=(0, 0, 15, 0)
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager"""
        self.add(wx.StaticLine(self._parent), create=False, margin=(0, 0, 15, 1))
