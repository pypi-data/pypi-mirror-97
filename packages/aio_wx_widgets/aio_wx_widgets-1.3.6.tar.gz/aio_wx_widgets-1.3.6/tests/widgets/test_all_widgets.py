import importlib
import inspect
import logging
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from aio_wx_widgets import widgets

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

IMAGE_PATH = Path(__file__).parent


def load_module(module_file: Path):
    """Load and import a module based on the location of the *.py file."""
    try:
        name = module_file.stem
        spec = importlib.util.spec_from_file_location(name, module_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as err:
        _LOGGER.exception(err)
        raise


def get_all_modules(package):
    """Yield all the modules from the provided package."""
    base = Path(inspect.getabsfile(package)).parent

    for fl in base.glob("*.py"):
        print(f"loading module {fl}")
        yield load_module(fl)


def get_all_classes_defined_in_module(module):
    """Return a tuple with the name of the class and the class object to be
    instantiated."""
    for _cls in inspect.getmembers(module, inspect.isclass):
        if module.__name__ == _cls[1].__module__:
            yield _cls


def get_all_widget_classes(package):
    for module in get_all_modules(package):
        for _cls in get_all_classes_defined_in_module(module):
            name, cls = _cls
            if name.startswith("_"):
                continue

            kwargs = {}
            if name == "AioButton":
                kwargs["label"] = "a label"
                kwargs["callback"] = Mock()
            elif name == "Group":
                kwargs["label"] = "grouplabel"
            elif name == "Entry":
                kwargs["binding"] = Mock()
            elif name == "Select":
                kwargs["choices"] = [Mock()]
            elif name == "CheckBox":
                kwargs["label"] = "checkbox_label"
                kwargs["binding"] = Mock()
            elif name == "LabelledItem":
                kwargs["label_text"] = "labeltext"
                kwargs["item"] = Mock()
            elif name == "Image":
                kwargs["image"] = Path(IMAGE_PATH / "phoenix_main.png")
            yield name, cls, kwargs


@pytest.mark.parametrize(
    "widget_class,kwargs",
    [
        pytest.param(_cls[1], _cls[2], id=_cls[0])
        for _cls in get_all_widget_classes(widgets)
    ],
)
def test_init(widget_class, kwargs, wx_app):
    widget_class(**kwargs)
