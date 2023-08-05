"""WX ui frames. A windows that holds a panel."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import wx

_LOGGER = logging.getLogger(__name__)


def get_app_icon_32(img_path: Path) -> wx.Icon:
    """Return an app icon that can be used as the top-left app icon.

    Use it from inside a wx.Frame: self.SetIcon(get_app_icon_32(icon_img))

    Returns:
        wx.Icon
    """
    app_icon_32 = wx.Icon()
    app_icon_32.CopyFromBitmap(wx.Bitmap(str(img_path), wx.BITMAP_TYPE_PNG))
    return app_icon_32


class DefaultFrame(wx.Frame):
    """A default frame for app windows.

    Always add a panel to this frame first.
    """

    def __init__(
        self,
        title,
        parent=None,
        size: wx.Size = None,
        style=None,
        icon_img: Optional[Path] = None,
    ):
        """Init.

        Args:
            title:
            parent:
            size:
            style:
        """
        kwargs = {}
        if style is not None:
            kwargs["style"] = style

        if size is None:
            size = wx.Size(800, 600)

        kwargs["size"] = size
        kwargs["title"] = title
        wx.Frame.__init__(self, parent, **kwargs)
        if icon_img:
            self.SetIcon(get_app_icon_32(icon_img))
        self._maximized = False
        self.view = None
        self.Bind(wx.EVT_CLOSE, self._on_close)
        # self.Bind(wx.EVT_MAXIMIZE, self._on_maximize)
        # self.Bind(wx.EVT_SIZE, self._on_restore)

    # pylint: disable=no-self-use
    def _on_close(self, evt):  # noqa
        _LOGGER.debug("Frame is closed.")
        evt.Skip()

    def _on_maximize(self, evt):
        if self.view:
            self._maximized = True
            self.view.ui_item.PostSizeEvent()
        evt.Skip()

    def _on_restore(self, evt):
        evt.Skip()
        if self.view:
            self.view.ui_item.PostSizeEvent()
