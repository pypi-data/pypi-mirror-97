# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Manual Test - set up some pages for viewing and interaction.
"""
import logging

import pygame

from gui import GUI
from page import Page
from pi_touch_gui._utilities import backlog_error
from raspberrypi_ts import Touchscreen
from test_pages.pages import get_pages

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] "
           "[%(name)s.%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z"
)
LOG = logging.getLogger(__name__)


def go_to_page(name):
    for page in pages:
        if page.name == name:
            return page
    return None


# Callback ping
def ping(gui, page):
    print(f"PING {page.name!r}")


if __name__ == "__main__":
    pygame.init()

    touchscreen = Touchscreen()
    interface = GUI(touchscreen)

    pages = get_pages()

    for page in pages:
        serialized_page = page.serialize()
        rehydrated_page = Page.deserialize(serialized_page)
        reserialized_page = rehydrated_page.serialize()
        pause = True

    for page in pages:
        functions = page.list_functions()
        print(f"PAGE {page.name!r} calls: {functions}")

    try:
        # Add any hardware or other initialization here
        interface.run(pages[0], callback=ping, cb_rate=1000)
    except Exception as e:
        backlog_error(e, f"Unmanaged exception {type(e)}: {e}")
    finally:
        # Add any hardware or other teardown here
        pass
