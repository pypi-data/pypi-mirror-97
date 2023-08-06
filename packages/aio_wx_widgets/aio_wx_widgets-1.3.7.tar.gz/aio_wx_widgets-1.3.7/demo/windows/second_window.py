import logging

from demo.controller import controller_two
from demo.model.demo_model import DemoModel
from demo.views.view_two import ViewTwo

from aio_wx_widgets.frame import DefaultFrame

_LOGGER = logging.getLogger(__name__)


class SecondWindow(DefaultFrame):
    def __init__(self):
        super().__init__("second window")

        model = DemoModel()
        controller = controller_two.ControllerTwo(model)
        view = ViewTwo(self, controller)
        view.populate()
