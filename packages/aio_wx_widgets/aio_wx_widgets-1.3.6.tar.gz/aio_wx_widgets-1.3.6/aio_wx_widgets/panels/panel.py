"""Panel. Sits in a frame. Holds widgets."""
from __future__ import annotations

import logging
from typing import Generic, TypeVar

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from aio_wx_widgets.core.sizers import PanelMixin, SizerMixin

_LOGGER = logging.getLogger(__name__)

#  pylint: disable=invalid-name
C = TypeVar("C")  # noqa


class SimplePanel(PanelMixin, SizerMixin, Generic[C]):
    """A simple panel.

    Consider this the main canvas to which widgets can be attached.
    """

    @property
    def ui_item(self):
        """Return UI item."""
        return self._ui_item

    @property
    def _sizer(self):
        return self._sizer_

    def __init__(self, parent, controller: C, scrollable=False, **kwargs):
        """Init."""
        self._controller = controller
        if scrollable:
            self._ui_item= ScrolledPanel(parent)
            self._ui_item.SetupScrolling()
        else:
            self._ui_item = wx.Panel(parent)
        super().__init__()

        self._sizer_ = wx.BoxSizer(wx.VERTICAL)
        self.ui_item.SetSizer(self._sizer)

        # useful for image updating layout
        self._ui_item.Parent.Bind(wx.EVT_SIZE, self._on_size)

    @property
    def controller(self) -> C:
        """Return the controller."""
        return self._controller

    def _on_size(self, evt):
        evt.Skip()
        self._refresh(evt)

    def _refresh(self,evt):

        _LOGGER.debug("posting size event")
        self._ui_item.PostSizeEvent()
