"""Datatypes used by widgets."""

import logging
from enum import Enum
from typing import Any, NamedTuple

import wx

_LOGGER = logging.getLogger(__name__)


class Choices(NamedTuple):
    """Choice item."""

    label: str
    value: Any


class HorAlign(Enum):
    """Horizontal alignment options."""

    left = wx.ALIGN_LEFT
    right = wx.ALIGN_RIGHT
    center = wx.ALIGN_CENTER_HORIZONTAL


class VerAlign(Enum):
    """Vertical alignment options."""

    top = wx.ALIGN_TOP
    bottom = wx.ALIGN_BOTTOM
    center = wx.ALIGN_CENTER_VERTICAL
