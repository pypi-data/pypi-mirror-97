import logging
from random import randint

from demo.windows import second_window, text_wrapping_window, third_window
from demo.windows.image_view_window import ImageViewWindow
from events import Events

from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)


class ControllerOne(BaseController):
    float_val: float = 0

    def __init__(self, model):
        # self.float_val: float = 0
        self.int_val: int = 987
        self.a_string_value = None
        self.a_checkbox_value: bool = True
        self.color_red = None
        self.ready = False
        super().__init__(model)

        self.add_to_log = Events()

    def _add_to_log(self, data: str):
        self.add_to_log.on_change(data)

    async def open_other_window(self):
        """Open a second window."""
        second_window.SecondWindow().Show()
        # _second_window.Show()
        _LOGGER.debug("Closed second window ?")

    async def open_third_window(self):
        third_window.Window().Show()

    async def open_text_wrapping_window(self):
        text_wrapping_window.TextWrappingWindow().Show()

    async def open_image_window(self):
        ImageViewWindow().Show()

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.int_val = val

    @property
    def value(self):
        return 10
