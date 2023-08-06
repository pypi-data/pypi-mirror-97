from __future__ import annotations

import logging
from random import randint
from typing import Sequence

from events import Events

from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.controller import BaseController
from aio_wx_widgets.core.data_types import Choices

_LOGGER = logging.getLogger(__name__)


class ControllerTwo(BaseController):
    def __init__(self, model):
        self.value_1: int = 0
        self.a_string_value = "A certain string"
        super().__init__(model)
        # self.create_task(self.value_setter())
        # self.add_to_log = Channel("Log messages")
        self.add_to_log = Events()
        self.choices: Sequence[T.Choice] = [
            Choices(label="choice 1", value={"value": 1}),
            Choices(label="choice 2", value={"value": 2}),
        ]
        self.selected_item = self.choices[0]
        self.selected_item2 = None

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.value_1 = val

    # async def value_setter(self):
    #     try:
    #         while 1:
    #             val = str(randint(1, 100))
    #             _LOGGER.debug("Setting value to : %s", val)
    #             self.add_to_log.publish(val)
    #             await asyncio.sleep(2)
    #     except CancelledError:
    #         _LOGGER.debug("Stopping value setter task.")
