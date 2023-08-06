from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from aio_wx_widgets.colors import BLACK, RED
from aio_wx_widgets.containers import Group
from aio_wx_widgets.containers.grid import VERTICAL, Grid
from aio_wx_widgets.containers.group import Section
from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.core.data_types import HorAlign, VerAlign
from aio_wx_widgets.core.validators import float_validator, int_validator
from aio_wx_widgets.panels.panel import SimplePanel
from aio_wx_widgets.widgets.button import AioButton
from aio_wx_widgets.widgets.checkbox import CheckBox
from aio_wx_widgets.widgets.experimental.fixed_grid import FixedGrid
from aio_wx_widgets.widgets.image import Image
from aio_wx_widgets.widgets.labelled_item import LabelledItem
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import Entry

if TYPE_CHECKING:
    from demo.controller.controller_one import ControllerOne

_LOGGER = logging.getLogger(__name__)

IMAGE_FOLDER = (Path(__file__).parent) / "image"


def _bool_to_color(value) -> int:
    """Convert a boolean to a color value.

    Used in a binding.
    """
    if value is True:
        return RED
    return BLACK


class ViewOne(SimplePanel["ControllerOne"]):
    def __init__(self, parent, controller: "ControllerOne"):
        super().__init__(parent, controller, scrollable=True)

    def populate(self):
        """Populate this view."""

        # Use a context manager for container types like a group or grid.
        # A group is a container with a label and a sizer inside. Inside
        # this sizer widgets, or other containers can be placed.
        # with self.add(DynamicGrid(), weight=1, margin=0) as fixed:
        #     fixed.add(Text("Col1"),col=0)
        #     fixed.add(Text("col2"),col=1)
        #     # fixed.add(Image(IMAGE_FOLDER / "phoenix_main.png"))

        with self.add(FixedGrid(), weight=1, margin=0) as fixed:
            fixed.add(Text("Col1"))
            fixed.add(Text("col2"))
            fixed.add(Image(IMAGE_FOLDER / "phoenix_main.png"))

        with self.add(Group("label")) as group:
            group.add(Text(binding=self.bind("int_val"), wrap=True), margin=20)
            # with group.add(Group("other group")) as grp:
            #     grp.add(Text(text="more text"))
            # with group.add(Section("section inside group")) as sec:
            #     sec.add(Text(text="section inside group"))
            # with group.add(Grid(orientation=Grid.VER),weight=1) as grd:
            #     grd.add(Text("This is long text", min_width=50))
            #     grd.add(Text("short", min_width=50))

        self.add(
            LabelledItem(
                "Label text",
                Entry(binding=self.bind("float_val"), validator=float_validator),
            )
        )

        with self.add(Section("Float validators")) as sc:
            sc.add(
                LabelledItem(
                    "Enter a float value",
                    Entry(binding=self.bind("float_val"), validator=float_validator,),
                    item_weight=2,
                )
            )
            with sc.add(Grid()) as grd:
                # the binding binds to an attribute defined in the controller
                # the weight determines how much space a specific item should consume
                # with respect to the other members of the container.

                grd.add(
                    Entry(binding=self.bind("float_val"), validator=float_validator,),
                    weight=4,
                )
                grd.add(
                    Text(binding=self.bind("float_val")),
                    weight=4,
                    ver_align=VerAlign.center,
                )
        with self.add(Section("Int validators")) as sc:
            sc.add(Text("Only integer values are allowed."))
            with sc.add(Grid()) as grd:
                grd.add(
                    Entry(binding=self.bind("int_val"), validator=int_validator,),
                    weight=3,
                    margin=0,
                )
                grd.add(
                    Entry(binding=self.bind("int_val"), validator=int_validator,),
                    weight=1,
                    margin=0,
                )
                grd.add(Text(binding=self.bind("int_val")), weight=1, margin=0)

        with self.add(Section("Bindings")) as sec:
            with sec.add(Grid()) as grd:
                grd.add(
                    Text(
                        "Use a converter with a binding to bind different types "
                        "of properties. Bind a color to a boolean using a converter.",
                        wrap=True,
                    ),
                    weight=1,
                )
                with grd.add(Grid(), weight=1) as grd1:
                    grd1.add(CheckBox("RED", self.bind("color_red")))
                    grd1.add(
                        Text(
                            text="This is text with a color binding",
                            color=self.bind("color_red", converter=_bool_to_color),
                        )
                    )
            with sec.add(Grid()) as grd:
                grd.add(
                    Text("Bind to the enabled property of a widget."),
                    weight=1,
                    ver_align=VerAlign.center,
                )
                with grd.add(Grid(), weight=1) as items:
                    btn = items.add(AioButton("toggle", self._toggle))
                    print(btn.ui_item.Parent)
                    items.add(
                        AioButton("toggle", self._toggle, enabled=self.bind("ready"))
                    )
                    items.add(
                        Entry(self.bind("a_string_value"), enabled=self.bind("ready"))
                    )
        with self.add(Grid()) as grd:
            grd.add(Entry(binding=Binding(self._controller, "a_string_value")))
            grd.add(Entry(binding=Binding(self._controller, "a_string_value")))

        with self.add(Grid()) as grd:
            grd.add(AioButton("button one", self._set_value), weight=6)
            grd.add(AioButton("button two,self", self._set_value), weight=6)

        with self.add(Section("Layout")) as grp:
            with grp.add(Grid()) as grd:
                grd.add(
                    Text(text="Widget, right & center alignment"),
                    weight=3,
                    hor_align=HorAlign.right,
                    ver_align=VerAlign.center,
                )
                with grd.add(Grid(VERTICAL), weight=6, margin=0) as vert_grid:
                    vert_grid.add(
                        AioButton("Left aligned button", self._set_value),
                        hor_align=HorAlign.left,
                        margin=4,
                    )
                    vert_grid.add(
                        AioButton(
                            "No Aligned widget (button in this case)", self._set_value
                        )
                    )
                    vert_grid.add(
                        Text(text="Center aligned widget with a large margin."),
                        margin=(10, 10, 30, 5),
                        hor_align=HorAlign.center,
                    )
                    vert_grid.add(
                        Text(
                            text="Text widget with centered text",
                            hor_align=Text.HOR_CENTER,
                        )
                    )
                    vert_grid.add(
                        AioButton(
                            "right aligned button.",
                            self._set_value,
                            enabled=self.bind("a_checkbox_value"),
                        ),
                        weight=2,
                        hor_align=HorAlign.right,
                    )

        self.add(CheckBox("A checkbox", binding=self.bind("a_checkbox_value")))
        self.add(
            CheckBox("The same checkbox value", binding=self.bind("a_checkbox_value"))
        )
        self.add(AioButton("open other window", self._on_open_second_window))
        self.add(AioButton("open third window", self._on_open_third_window))
        self.add(
            AioButton("open text wrapping window", self._on_open_text_wrapping_window)
        )
        self.add(AioButton("Open image view", self._on_open_image_view))

    def _toggle(self, evt):
        self.controller.ready = not self.controller.ready

    async def _on_open_second_window(self, evt):
        await self._controller.open_other_window()

    async def _on_open_third_window(self, evt):
        await self._controller.open_third_window()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _on_open_text_wrapping_window(self, evt):
        await self._controller.open_text_wrapping_window()

    async def _on_open_image_view(self, evt):
        await self._controller.open_image_window()

    async def _set_value(self, evt):
        await self._controller.set_value()
