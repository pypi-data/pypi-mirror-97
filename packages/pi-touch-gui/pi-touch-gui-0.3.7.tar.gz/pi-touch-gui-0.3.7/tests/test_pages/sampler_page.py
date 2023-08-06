# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - Widget Sample, all the widgets, configured for keyboard grid.
"""

import pygame

from colors import (WHITE, MEDIUM_GRAY, BLUE, RED, BLACK, DARK_RED, GREEN,
                    CYAN, MAGENTA)
from page import Page
from pi_touch_gui.widget_buttons import Button, ButtonGroup
from pi_touch_gui.widget_controls import Dial, Slider
from pi_touch_gui.widget_displays import Indicator, Label, Graph
from pi_touch_gui.widget_functions import (ButtonFunction, IndicatorFunction,
                                           GraphFunction,
                                           DialFunction, SliderFunction,
                                           )
from tests._utilities import fake_data_graph_function, button_to_page


# =========================================================
# Hold-behavior buttons and indicator
# =========================================================

def _up_dn_button_func(**kwargs):
    if kwargs['state']:
        _up_down_flag = kwargs['direction']
    else:
        _up_down_flag = 0

    page = kwargs['page']
    data = page.widget_data
    data['up_down'] = _up_down_flag


def _up_dn_indicator_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    _up_down_flag = data.get('up_down', 0)

    if _up_down_flag == 0:
        return False, ''
    elif _up_down_flag == 1:
        return True, "UP"
    else:
        return True, "DN"


_up_button = Button(
    (115, 105), (60, 50),
    label="^",
    behavior=Button.HOLD,
    style=Button.OBROUND,
    function=ButtonFunction(_up_dn_button_func,
                            {'direction': 1}))

_up_dn_indicator = Indicator(
    (115, 160), (60, 50),
    label_color2=WHITE,
    function=IndicatorFunction(_up_dn_indicator_func))

_dn_button = Button(
    (115, 215), (60, 50),
    label="v",
    behavior=Button.HOLD,
    style=Button.OBROUND,
    function=ButtonFunction(_up_dn_button_func,
                            {'direction': -1}))

# =========================================================
# Rounded Button styles
# =========================================================

_back_button = Button((110, 400), (75, 50),
                      label="Back",
                      style=Button.LEFT_ROUND,
                      function=ButtonFunction(button_to_page,
                                              {'to_page': 'entry'}))

_do_nothing_button = Button((190, 400), (150, 50),
                            label="Do Nothing",
                            style=Button.RECTANGLE,
                            color1=MEDIUM_GRAY, color2=WHITE,
                            label_color1=BLUE, label_color2=RED)

_next_button = Button((345, 400), (75, 50),
                      label="Next",
                      style=Button.RIGHT_ROUND,
                      function=ButtonFunction(button_to_page,
                                              {'to_page': 'power_off'}))


# ---- Boop button, for some amusement

def _boop_button_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    boop_count = data.get('boop_count', 4) - 1
    data['boop_count'] = boop_count


def _boop_indicator_func(**kwargs):
    """ Countdown; when we reach 0, we exit the program.
    """
    page = kwargs['page']
    data = page.widget_data
    boop_count = data.get('boop_count', 4)
    if boop_count == 4:
        return False, ''
    if boop_count == 0:
        exit(0)
    return True, f"{boop_count}"


_boop_button = Button(
    (430, 400), (50, 50),
    label="X",
    style=Button.OBROUND,
    function=ButtonFunction(_boop_button_func))

_boop_indicator = Indicator(
    (485, 400), (50, 50),
    color1=BLACK, color2=RED,
    label_color1=WHITE, label_color2=BLACK,
    function=IndicatorFunction(_boop_indicator_func))


# =========================================================
# Toggle-behavior Buttons with reset
# =========================================================

def _reset_count_buttons(**kwargs):
    page = kwargs['page']
    _one_button.clear(page)
    _two_button.clear(page)
    _three_button.clear(page)


_count_buttons_label = Label((190, 105), (100, 25),
                             label="Pick Several")
_one_button = Button(
    (190, 130), (100, 50),
    label="One",
    behavior=Button.TOGGLE)
_two_button = Button(
    (190, 185), (100, 50),
    label="Two",
    behavior=Button.TOGGLE)
_three_button = Button(
    (190, 240), (100, 50),
    label="Three",
    behavior=Button.TOGGLE)
_count_reset_button = Button(
    (190, 295), (100, 50),
    label='RESET',
    label_color1=DARK_RED,
    function=ButtonFunction(_reset_count_buttons))

# =========================================================
# Button Group
# =========================================================

_color_buttons_label = Label(
    (300, 105), (100, 25),
    label="Pick One")

_red_button = Button(
    (300, 130), (100, 50),
    label="Red",
    color2=RED,
    behavior=Button.TOGGLE)
_green_button = Button(
    (300, 185), (100, 50),
    label="Green",
    color2=GREEN,
    behavior=Button.TOGGLE)
_blue_button = Button(
    (300, 240), (100, 50), label="Blue",
    color2=BLUE,
    behavior=Button.TOGGLE)

_color_group = ButtonGroup([_red_button, _green_button, _blue_button])


# =========================================================
# Controls and Graphs
# =========================================================

# ---- Graph and Control Functions

def _dial_control_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    data['dial_value'] = kwargs['value']


def _slider_h_control_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    data['slider_h_value'] = kwargs['value']


def _slider_v_control_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    data['slider_v_value'] = kwargs['value']


def _graph_update_func(**kwargs):
    page = kwargs['page']
    data = page.widget_data
    size = kwargs['num']

    last_track_update = data.get('last_track_update', pygame.time.get_ticks())
    track_1_data = data.get('track_1_data', [])
    track_2_data = data.get('track_2_data', [])
    track_3_data = data.get('track_3_data', [])
    max_track_samples = data.get('max_track_samples', 1000)

    dial_value = data.get('dial_value', 0)
    slider_h_value = data.get('slider_h_value', 0)
    slider_v_value = data.get('slider_v_value', 0)

    # Update the graph
    time = pygame.time.get_ticks()
    # Update twice per second, to show some life
    if (time - last_track_update) > 250:
        track_1_data.append(dial_value)
        track_2_data.append(slider_h_value)
        track_3_data.append(slider_v_value)
        last_track_update = time

    # Truncate to the maximum size to prevent memory crash
    if len(track_1_data) > max_track_samples:
        track_1_data = track_1_data[-max_track_samples:]
        track_2_data = track_2_data[-max_track_samples:]
        track_3_data = track_3_data[-max_track_samples:]

    # Make sure the widget data is initialized
    data.update({
        'last_track_update': last_track_update,
        'track_1_data': track_1_data,
        'track_2_data': track_2_data,
        'track_3_data': track_3_data,
        'max_track_samples': max_track_samples
    })

    # Return what was asked for
    return [{"color": CYAN, "data": track_1_data[-size:]},
            {"color": MAGENTA, "data": track_2_data[-size:]},
            {"color": BLUE, "data": track_3_data[-size:]}, ]


# ---- Graph and Control Widgets

_control_graph = Graph(
    (410, 130), (390, 100), min_max=(0, 100),
    function=GraphFunction(_graph_update_func))
_control_dial = Dial((450, 240), (150, 150), min_max=(0, 100),
                     start_value=50, snap_value=1,
                     color2=CYAN,
                     dynamic=True, function=DialFunction(_dial_control_func))
_h_slider = Slider((620, 400), (150, 50),
                   min_max=(25, 75), start_value=40,
                   snap_value=5,
                   label_color1=BLACK, color1=MEDIUM_GRAY, color2=MAGENTA,
                   dynamic=True,
                   function=SliderFunction(_slider_h_control_func))
_v_slider = Slider((620, 240), (50, 150),
                   min_max=(0, 100), start_value=60,
                   snap_value=.1,
                   label_color1=BLACK, color1=MEDIUM_GRAY, color2=BLUE,
                   dynamic=False,
                   function=SliderFunction(_slider_v_control_func))
_fake_graph = Graph((680, 240), (110, 150), min_max=(-100, 100),
                    quiet=True,
                    function=GraphFunction(fake_data_graph_function))


# =========================================================
# Page configuration and definition
# =========================================================


def sampler_page(background):
    # Tests background image, Button, RoundedButton, DynamicButton,
    # ToggleButton, ButtonGroup, Label, Indicator, ...
    _sampler_page = Page('sampler',
                         background=background,
                         widgets=[
                             _up_dn_indicator, _up_button, _dn_button,
                             _back_button, _do_nothing_button, _next_button,
                             _boop_button, _boop_indicator,

                             _count_buttons_label,
                             _one_button, _two_button, _three_button,
                             _count_reset_button,

                             _color_buttons_label,
                             _red_button, _green_button, _blue_button,
                             _color_group,

                             _control_graph, _control_dial, _v_slider,
                             _h_slider,
                             _fake_graph
                         ])

    return _sampler_page
