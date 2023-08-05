"""Error messages.

Used in combination with validators.
"""

import logging

import wx

from aio_wx_widgets.const import ERROR_COLOR

_LOGGER = logging.getLogger(__name__)


class ErrorPopup(wx.PopupWindow):
    """A popup.

    Opens near the widget when a validation error occurs.
    """

    def __init__(self, parent, content, style=0):
        super().__init__(parent, style)
        panel = wx.Panel(self)
        panel.SetBackgroundColour(ERROR_COLOR)
        message = wx.StaticText(panel, -1, content)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(message, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()
