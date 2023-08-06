import asyncio
import logging

import pytest

from aio_wx_widgets.frame import DefaultFrame

_LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "kwargs,results",
    [
        ({"title": "a title"}, {"title": "a title", "width": 800, "height": 600}),
        (
            {"title": "a title", "size": (300, 200)},
            {"title": "a title", "width": 300, "height": 200},
        ),
    ],
)
def test_frame_initialize(wx_app, kwargs, results):
    """smoke test initializing the frame."""

    frame = DefaultFrame(**kwargs)

    assert frame.Title == results["title"]

    assert frame.Size.Width == results["width"]
    assert frame.Size.Height == results["height"]


@pytest.mark.asyncio
async def test_on_close_event(wx_app, mocker):
    """Test whether the _on_close callback is called when frame gets closed."""
    mocker.patch.object(DefaultFrame, "_on_close")
    frame = DefaultFrame(title="a title")
    frame.Close()
    await asyncio.sleep(0.1)
    frame._on_close.assert_called_once()
