from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import wx

from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.containers import Section
from aio_wx_widgets.containers.grid import VERTICAL, Grid
from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.core.data_types import HorAlign
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets import LabelledItem
from aio_wx_widgets.widgets.button import AioButton
from aio_wx_widgets.widgets.select import Select
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import Entry

if TYPE_CHECKING:
    from demo.controller.controller_two import ControllerTwo

_LOGGER = logging.getLogger(__name__)


class ViewTwo(SimplePanel["ControllerTwo"]):
    """Second view."""

    def __init__(self, parent, controller: ControllerTwo):
        self._controller = controller
        super().__init__(parent, controller)
        self._text = Text("This is text that changes as a result of an event happening")

        # self._controller.add_task(self._controller.add_to_log.subscribe(self._add_to_log))
        self.controller.add_to_log.publish += self._add_to_log

        self._callback_text = Text("Nothing selected yet")
        # self._bound_selected_item = Text("Nothing selected yet")

    def populate(self):
        with self.add(Section("Labelled items.")) as sec:
            sec.add(Text("default labelled item:"))
            sec.add(
                LabelledItem(
                    "Item",
                    Select(
                        self.controller.choices,
                        on_select_callback=self._on_select_callback,
                    ),
                )
            )

            l_item = LabelledItem(
                "Item",
                Select(self._controller.choices, binding=self.bind("selected_item")),
                align_right=False,
            )
            sec.add(Text(str(l_item)))
            sec.add(l_item)
            l_item = LabelledItem(
                "Item",
                Select(self._controller.choices, binding=self.bind("selected_item")),
                item_weight=2,
            )
            sec.add(Text(str(l_item)))
            sec.add(l_item)
            l_item = LabelledItem(
                "Item",
                Select(self._controller.choices, binding=self.bind("selected_item")),
                item_weight=2,
                item_alignment=HorAlign.left,
            )
            sec.add(Text(str(l_item)))
            sec.add(l_item)
        with self.add(Section("Selectable, bound to None")) as sec:
            sec.add(
                Select(self._controller.choices, binding=self.bind("selected_item2"))
            )
            sec.add(Text(binding=self.bind("selected_item2")))

        self.add(
            Entry(binding=Binding(self._controller, "value_1")), margin=(10, 10, 5, 20),
        )
        self.add(Entry(binding=Binding(self._controller, "value_1")))
        self.add(
            AioButton("test button with normal function as callback", self._press),
            margin=(10, 10, 5, 20),
        )
        self.add(self._text)

        # It is possible to add bare wx-python widgets.
        self.add(wx.StaticLine(parent=self.ui_item), create=False)

        with self.add(Grid()) as grd:
            grd.add(
                Text("This is a selection dropdown"),
                weight=4,
                hor_align=HorAlign.right,
            )
            with grd.add(Grid(orientation=VERTICAL), weight=6) as grd:
                grd.add(
                    Select(
                        self.controller.choices,
                        on_select_callback=self._on_select_callback,
                        binding=self.bind("selected_item"),
                    ),
                    hor_align=HorAlign.left,
                )
                grd.add(Text("Selection based on callback:"))
                grd.add(self._callback_text)
                grd.add(Text("Selection based on binding value:"))
                grd.add(Text(binding=self.bind("selected_item")))
                # grd.add(
                #     AioButton(
                #         label="Display bound value", callback=self._show_bound_value
                #     )
                # )
                # grd.add(self._bound_selected_item)

    # def _show_bound_value(self, evt):
    #     self._bound_selected_item.set_text(self._controller.selected_item)

    def _on_select_callback(self, choice: T.Choice):
        self._callback_text.set_text(str(choice))

    def _press(self, evt):
        self._add_to_log("button pressed.")

    def _add_to_log(self, item: str):
        self._text.set_text(item)
