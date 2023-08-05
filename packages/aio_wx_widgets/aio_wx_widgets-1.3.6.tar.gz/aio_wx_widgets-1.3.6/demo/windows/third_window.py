import logging

from demo.controller import controller_three
from demo.model.demo_model import DemoModel
from demo.views.view_three import ViewThree

from aio_wx_widgets.frame import DefaultFrame

_LOGGER = logging.getLogger(__name__)


class Window(DefaultFrame):
    def __init__(self):
        super().__init__("third window")

        model = DemoModel()
        controller = controller_three.ControllerThree(model)
        view = ViewThree(self, controller)
        view.populate()
