import logging

import pytest

from aio_wx_widgets.core.data_types import HorAlign
from aio_wx_widgets.core.sizers import _align_item, wx

_LOGGER = logging.getLogger(__name__)


class MockBoxSizer:
    def __init__(self, orient=wx.HORIZONTAL):
        self.orient = orient
        self.item = None
        self.weight = None
        self.layout = None

    def Add(self, item, weight, orientation, layout):
        self.item = item
        self.weight = weight
        self.orient = orientation
        self.layout = layout


@pytest.fixture
def box_sizer(mocker):
    mocker.patch.object(wx, "BoxSizer", MockBoxSizer)


class UiItem:
    """A mocked ui item"""


def test_align_no_alignment(box_sizer):
    al = _align_item(UiItem(), wx.VERTICAL, None, None, current_layout=0)

    assert isinstance(al[0], UiItem)


def test_align_hor_alignment_vert_sizer(box_sizer):
    """No sizer used for wrapping the ui"""
    al = _align_item(UiItem(), wx.VERTICAL, HorAlign.center, None, current_layout=0)
    assert isinstance(al[0], UiItem)


def test_aling_hor_alignment_hor_sizer(box_sizer):
    """A sizer will be used to make the horizontal alignment happen."""

    al = _align_item(UiItem(), wx.HORIZONTAL, HorAlign.right, None, current_layout=0)

    assert isinstance(al[0], MockBoxSizer)
    assert isinstance(al[0].item, UiItem)
