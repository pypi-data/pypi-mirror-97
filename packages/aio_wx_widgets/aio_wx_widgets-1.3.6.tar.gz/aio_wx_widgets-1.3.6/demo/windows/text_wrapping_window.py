import logging

from demo.controller import text_wrapping_controller
from demo.model.demo_model import DemoModel
from demo.views import text_wrapping

from aio_wx_widgets.frame import DefaultFrame

_LOGGER = logging.getLogger(__name__)


class TextWrappingWindow(DefaultFrame):
    def __init__(self):
        super().__init__("Text wrapping window")

        model = DemoModel()
        controller = text_wrapping_controller.TextWrappingController(model)
        view = text_wrapping.TextWrappingView(self, controller)
        view.populate()
