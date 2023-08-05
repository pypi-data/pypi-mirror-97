"""A labelled item."""

import logging

from aio_wx_widgets.containers.grid import Grid
from aio_wx_widgets.core.data_types import HorAlign, VerAlign
from aio_wx_widgets.widgets.text import Text

_LOGGER = logging.getLogger(__name__)

__all__ = ["LabelledItem"]


class LabelledItem(Grid):
    """Labelled item."""

    def __init__(
        self,
        label_text: str,
        item,
        align_right=True,
        label_weight=1,
        item_weight=1,
        item_alignment=None,
    ):
        super().__init__()
        self.label_text = label_text
        self._item = item
        self._label_weight = label_weight
        self._item_weight = item_weight
        self.align_right = align_right
        self._item_alignment = item_alignment

    def init(self, parent):
        super().init(parent)
        if self.align_right:
            hor_alignment = HorAlign.right
        else:
            hor_alignment = None
        self.add(
            Text(self.label_text),
            weight=self._label_weight,
            hor_align=hor_alignment,
            ver_align=VerAlign.center,
        )
        self.add(self._item, weight=self._item_weight, hor_align=self._item_alignment)

    def __call__(self, parent, *args, **kwargs):
        self.init(parent)
        return self

    def __str__(self):
        return (
            f"{self.__class__.__name__}, "
            f"label_weigth({self._label_weight}), "
            f"item_weight({self._item_weight}), "
            f"align_right({self.align_right}), "
            f"item_alignment({self._item_alignment})"
        )
