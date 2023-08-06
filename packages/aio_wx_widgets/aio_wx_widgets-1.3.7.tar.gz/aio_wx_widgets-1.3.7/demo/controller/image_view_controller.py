import logging

from aio_wx_widgets.controller import BaseController

_LOGGER = logging.getLogger(__name__)


class ImageViewController(BaseController):
    def __init__(self, model):
        super().__init__(model)
