from __future__ import annotations

import logging

from demo.controller.controller_three import ControllerThree

from aio_wx_widgets.containers.grid import Grid
from aio_wx_widgets.containers.group import Group
from aio_wx_widgets.core.binding import Binding
from aio_wx_widgets.core.sizers import PanelMixin, SizerMixin
from aio_wx_widgets.panels.splitter_panel import TwoSplitterWindow
from aio_wx_widgets.widgets.button import AioButton
from aio_wx_widgets.widgets.text import Text
from aio_wx_widgets.widgets.text_entry import Entry

_LOGGER = logging.getLogger(__name__)

_LONG_TEXT = "This is a long text that actually should wrap properly and right from the start. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. This is the last text."


class SplitterWindow(TwoSplitterWindow, PanelMixin, SizerMixin):
    def __init__(
        self,
        parent,
        controller: ControllerThree,
        scrollable=False,
        window_one_width=250,
    ):
        super().__init__(
            parent, splitter_one_scrollable=False, splitter_two_scrollable=False
        )
        self._controller = controller
        # self.splitter_window_two.add(Text("This is text"))
        self.splitter_window_two.add(Entry(self.bind("value_1")))

    @property
    def controller(self):
        return self._controller


class ViewThree(SplitterWindow):
    def __init__(self, parent, controller):
        self._controller = controller
        super().__init__(parent, controller, scrollable=False)

        self.split_button = AioButton("Remove split", self._toggle_window_2)
        self._toggle_state = True

    @property
    def controller(self):
        return self._controller

    def populate(self):
        """Populate this view."""
        self.splitter_window_one.add(Entry(binding=self.bind("value_1")), margin=20)
        # Use a context manager for container types like a group or grid.
        # A group is a container with a label and a sizer inside. Inside
        # this sizer widgets, or other containers can be placed.
        with self.splitter_window_one.add(Group("A labelled container.")) as group:
            # group.add(Text(text="A horizontal grid."))

            with group.add(Grid()) as grd:
                # the binding binds to an attribute defined in the controller
                # the weight determines how much space a specific item should consume
                # with respect to the other members of the container.
                grd.add(Entry(binding=self.bind("value_1")), weight=3, margin=3)
                grd.add(Entry(binding=self.bind("value_1")), weight=1, margin=3)
                grd.add(Entry(binding=self.bind("value_1")), weight=1, margin=3)

        with self.add(Group("Any text entry.")) as group:
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))
            group.add(Entry(binding=Binding(self._controller, "a_string_value")))

        with self.add(Grid()) as grd:
            grd.add(AioButton("button one", self._set_value), weight=6)
            grd.add(AioButton("button two,self", self._set_value), weight=6)

        self.add(Text(_LONG_TEXT, wrap=True))

        with self.add(Grid()) as grd:
            grd.add(AioButton("toggle", self._toggle))
            self._btn = grd.add(
                AioButton("toggle", self._toggle, enabled=self.bind("ready"))
            )
            grd.add(Entry(self.bind("bound_text"), enabled=self.bind("ready")))

        self._set_split_button_text()
        # self.ui_item.PostSizeEvent()

    def _toggle(self, evt):
        self.controller.ready = not self.controller.ready

    def _set_split_button_text(self):
        if self.is_split:
            self.split_button.label = "Close"
        else:
            self.split_button.label = "Open"

    def _toggle_window_2(self, evt):
        if self.is_split:
            self.hide_window2()
        else:
            self.show_window2()
        self._set_split_button_text()

    async def _on_open(self, evt):
        await self._controller.open_other_window()

    async def _set_value(self, evt):
        await self._controller.set_value()
