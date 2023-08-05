"""Image widget."""

import logging
from pathlib import Path

import wx

from aio_wx_widgets.colors import RED
from aio_wx_widgets.const import is_debugging
from aio_wx_widgets.core.base_widget import BaseWidget

_LOGGER = logging.getLogger(__name__)

__all__ = ["Image"]


def _get_ratio(image: wx.Image):
    size = image.GetSize()
    width_height = size[0] / size[1]
    return width_height


class _SizeableImage(wx.StaticBitmap):
    """A static bitmap child.

    The DoGetBestClientSize override method ensures that the proper image size
    is set once its parent(s) start resizing.
    """

    def __init__(self, *args, **kwargs):
        self._image_ratio = kwargs.pop("ratio")
        self._image = kwargs.pop("image")
        self._min_width = 10
        self._prev_image_size = (-1, -1)

        super().__init__(*args, **kwargs)
        if is_debugging():
            self.SetBackgroundColour(RED)

    def _set_image(self, size):
        """Set the image."""
        if size[0] <= 0 or size[1] <= 0:
            _LOGGER.debug("Image size has 0 value. Skipping")
            return
        if self._prev_image_size == size:
            _LOGGER.debug("Skipping image resize")
            return

        self._prev_image_size = size
        _LOGGER.debug("Setting image size to : %s", size)
        image = self._image.Scale(size[0], size[1], quality=wx.IMAGE_QUALITY_BICUBIC)
        bitmap = wx.Bitmap(image)

        self.SetBitmap(bitmap)

    # pylint: disable=invalid-name
    def DoGetBestClientSize(self):
        """Return best image size when parent sizer is re-arranging children."""
        item_size = self.GetSize()
        _LOGGER.debug("Image size %s", item_size)

        min_x = item_size[0]

        optimal_size = (-1, int(min_x / self._image_ratio))
        image_size = (min_x, optimal_size[1])
        # if not image_size == self._prev_image_size:
        self._set_image(image_size)

        return optimal_size


class Image(BaseWidget):
    """Autoscaling image widget.

    The image will resize once it is put inside a boxsizer (or aio-wx-widget grid).
    """

    def __init__(self, image: Path, min_width=10, max_width=None):
        """Init.

        Args:
            image: The image to be displayed.
            min_width: The minimal allowed image size.
            max_width: Max allowed image width.
        """
        self._image = wx.Image(str(image), wx.BITMAP_TYPE_PNG)
        self._image_ratio = _get_ratio(self._image)
        super().__init__(
            _SizeableImage(ratio=self._image_ratio, image=self._image),
            min_width=min_width,
            value_binding=None,
        )

    def init(self, parent):
        self.ui_item.Create(parent)

        # parent.Bind(wx.EVT_SIZE, self._on_size)
        # parent.PostSizeEvent()

    def __call__(self, parent):
        self.init(parent)
        return self

    # def _on_size(self, evt):  # noqa
    #     evt.Skip()
    #     self.ui_item.InvalidateBestSize()
    #     self.ui_item.Layout()
