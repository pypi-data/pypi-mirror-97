import asyncio
import logging
import os

from demo.windows.main_window import MainWindow
from wxasync import WxAsyncApp

_LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    os.environ["DEBUGGING"] = "1"
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    app = WxAsyncApp()
    main_window = MainWindow()
    main_window.Show()
    app.SetTopWindow(main_window)
    loop.run_until_complete(app.MainLoop())
