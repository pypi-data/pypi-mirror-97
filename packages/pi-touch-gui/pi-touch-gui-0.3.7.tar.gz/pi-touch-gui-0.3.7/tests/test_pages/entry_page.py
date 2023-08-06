# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - An entry page with pulsing lights
"""

# ---- Pulsing light test function (light)

from colors import RED
from page import Page
from pi_touch_gui.widget_buttons import Button
from pi_touch_gui.widget_displays import Light, Label
from pi_touch_gui.widget_functions import ButtonFunction, LightFunction
from tests._utilities import pulsing_light_func, button_to_page

_left_label = Label((20, 50), (100, 50),
                    label="L", label_alignment=Label.LEFT)
_center_label = Label((20, 100), (100, 50),
                      label="C", label_alignment=Label.CENTER)
_right_label = Label((20, 150), (100, 50),
                     label="R", label_alignment=Label.RIGHT)

_entry_label = Label((0, 0), (800, 50), label="ENTER")

_pulse1_light = Light((0, 0), (50, 50),
                      function=LightFunction(pulsing_light_func,
                                             {'rate': 400}))

_pulse2_light = Light((750, 0), (50, 50),
                      function=LightFunction(pulsing_light_func,
                                             {'rate': 300}))

_pulse3_light = Light((0, 430), (50, 50),
                      function=LightFunction(pulsing_light_func,
                                             {'rate': 200}))

_pulse4_light = Light((750, 430), (50, 50),
                      function=LightFunction(pulsing_light_func,
                                             {'rate': 100}))


def go_to_page_sampler(button, state):
    from tests.test_pages.pages import get_pages
    from tests._utilities import go_to_page
    return go_to_page(get_pages(), 'sampler')


_touch_me_button = Button((200, 150), (400, 100), font_size=100,
                          label_color1=RED, label="Touch Me",
                          function=ButtonFunction(button_to_page,
                                                  {'to_page': 'sampler'}))


def entry_page():
    # Tests dynamic Light functions, Label, and default Page function
    _entry_page = Page('entry', [
        _pulse1_light,
        _entry_label,
        _left_label,
        _center_label,
        _right_label,
        _pulse2_light,
        _pulse3_light,
        _pulse4_light,
        _touch_me_button
    ])
    return _entry_page
