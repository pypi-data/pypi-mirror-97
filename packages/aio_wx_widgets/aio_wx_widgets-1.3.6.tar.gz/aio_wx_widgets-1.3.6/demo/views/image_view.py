import logging
from pathlib import Path

from demo.controller.image_view_controller import ImageViewController

from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets import Text
from aio_wx_widgets.widgets.experimental.fixed_grid import DynamicGrid, FixedGrid
from aio_wx_widgets.widgets.image import Image

_LOGGER = logging.getLogger(__name__)

IMAGE_FOLDER = (Path(__file__).parent) / "image"


class ImageView(SimplePanel[ImageViewController]):
    """A text wrapping view test."""

    def populate(self):
        # self.add(Image(IMAGE_FOLDER / "phoenix_main.png"), weight=1)
        with self.add(DynamicGrid()) as grd:
            # grd.add_space()
            grd.add(Text("this is text"), col=1)
            grd.add(Image(IMAGE_FOLDER / "phoenix_main.png"), col=2, span=2)
            # grd.add(Text("this is text"), col=2)
        with self.add(FixedGrid()) as grd:
            # grd.add_space()
            grd.add(Text("this is text"))
            grd.add(Image(IMAGE_FOLDER / "phoenix_main.png"))
            grd.add(Text("this is text"))
        with self.add(DynamicGrid()) as grd:
            grd.add(Text("This is other test"), col=0)
            grd.add(Image(IMAGE_FOLDER / "phoenix_main.png"), col=1, span=2)
