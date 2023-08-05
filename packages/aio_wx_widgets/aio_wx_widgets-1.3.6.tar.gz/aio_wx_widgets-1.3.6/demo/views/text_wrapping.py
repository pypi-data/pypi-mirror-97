import logging

from aio_wx_widgets.widgets.experimental.fixed_grid import DynamicGrid, FixedGrid
from demo.controller.text_wrapping_controller import TextWrappingController

from aio_wx_widgets.containers import Grid
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets import Text, CheckBox
from demo.views.view_one import _bool_to_color

_LOGGER = logging.getLogger(__name__)

LONG_TEXT = 10 * "very very long text that should just wrap.."


class TextWrappingView(SimplePanel[TextWrappingController]):
    """A text wrapping view test."""

    def populate(self):

        # with self.add(Grid(), weight=1) as grd:
        #     with grd.add(Grid(orientation=Grid.VER), weight=2) as column_one:
        #         column_one.add(Text(text=LONG_TEXT, wrap=True), weight=1)
        #     with grd.add(Grid(orientation=Grid.VER), weight=1) as column_two:
        #         column_two.add_space()
        with self.add(DynamicGrid()) as grd:
            grd.add(Text(text=LONG_TEXT, wrap=True), col=1)
            grd.add_spacer(col=2)
        # with self.add(FixedGrid()) as grd:
        #     grd.add(Text(text=LONG_TEXT,wrap=True))
        #     grd.add(Text(text="place hoolder text"))
