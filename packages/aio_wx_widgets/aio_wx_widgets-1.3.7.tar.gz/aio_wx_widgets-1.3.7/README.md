

![CI](https://github.com/sander76/aio_wx_widgets/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/sander76/aio_wx_widgets/branch/master/graph/badge.svg)](https://codecov.io/gh/sander76/aio_wx_widgets)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# aio_wx_widgets

Wx python app structure using MVC model. Work in progress, adding widgets when I need them.
See the demo folder for usage.

Features:

- Add widgets using context managers.
- Two-way or one-way Property binding from controller properties to the view.
- Proper Margins and alignment of items

The example below is a bit outdated, but gives a rough idea. Please see the demo for more.

    ```python
    # Use a context manager for container types like a group or grid.
    # A group is a container with a label and a sizer inside. Inside
    # this sizer widgets, or other containers can be placed.
    with self.add(Group("A labelled container.")) as group:
        group.add(Text(text="A horizontal grid."))

        with group.add(Grid()) as grd:
            # the binding binds to an attribute defined in the controller
            # the weight determines how much space a specific item should consume
            # with respect to the other members of the container.
            grd.add(IntEntry(binding=self.bind("value_1")), weight=6, margin=3)
            grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)
            grd.add(IntEntry(binding=self.bind("value_1")), weight=4, margin=3)
    ```


    ```python 
    vert_grid.add(
        Text(text="Center aligned text with a large margin."),
        margin=(10, 10, 30, 5),  # (left,right,top,below)
        align_horizontal=AlignHorizontal.center,)
    ```

## Installation

- Create a virtual env, activate it and `pip install aio_wx_widgets`

## Running the demo

- Install the libary as described above.
- clone the repo.
- from the activated virtualenv: `python -m demo`
