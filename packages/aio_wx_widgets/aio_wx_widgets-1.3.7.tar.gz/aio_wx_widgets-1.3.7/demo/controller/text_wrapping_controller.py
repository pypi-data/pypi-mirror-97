import logging

from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)


class TextWrappingController(BaseController):
    def __init__(self, model):
        self.color_red = None
        super().__init__(model)
