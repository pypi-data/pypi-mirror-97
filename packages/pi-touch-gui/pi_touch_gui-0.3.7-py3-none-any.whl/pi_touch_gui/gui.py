# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Graphical User Interface objects

    A `Page` is a set of widgets that define the interaction and display
    surface of the GUI

    The `GUI` manages the hardware and runs the Pages
"""
import logging
from typing import NoReturn

import pygame

from pi_touch_gui._utilities import backlog_error
from pi_touch_gui.multitouch.raspberrypi_ts import Touchscreen

# from pi_touch_gui.page import Page

LOG = logging.getLogger(__name__)


class GUI(object):
    # Constants that define the GUI behavior
    FPS = 60
    FADE_TIME = 60
    BLACKOUT_TIME = 300
    BRIGHT_LEVEL = 128
    FADE_LEVEL = 16

    # Initialize the event timer
    last_event = pygame.time.get_ticks()

    def __init__(self, touchscreen, bright=None):
        """ A Graphical User Interface for using a touchscreen.

        Parameters
        ----------
        touchscreen : Touchscreen
            See for example the `multitouch.raspberrypi_ts.Touchscreen`
        bright : int
            Brightness level (to balance visibility and screen wear).  Defaults
            to GUI.BRIGHT_LEVEL.
        """
        self._bright_level = bright or self.BRIGHT_LEVEL
        self._touchscreen = touchscreen
        self._current_page = None
        self._first_page = None
        self._running = False
        self._faded = False
        self._blacked = False

        with open('/sys/class/backlight/rpi_backlight/max_brightness',
                  'r') as f:
            max_str = f.readline()
        self.max_brightness = min(int(max_str), 255)
        self.set_brightness(self._bright_level)

    def reset_display(self):
        """ Enable on the backlight and bring to the default brightness.
        """
        self.last_event = pygame.time.get_ticks()

        if self._faded:
            self.set_brightness(self._bright_level)
            self._faded = False
        if self._blacked:
            self.set_light(True)
            self._blacked = False

    def set_brightness(self, level):
        """ Set the backlight to a determined brightness level.

        Parameters
        ----------
        level : int
        """
        level_str = f"{min(self.max_brightness, level)}\n"
        with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as f:
            f.write(level_str)

    def set_light(self, on):
        """ Turn the backlight activateion to On or Off

        Parameters
        ----------
        on : bool
            True for On, False for Off
        """
        if on is True:
            blank_str = "0"
        else:
            blank_str = "1"
            self._current_page = self._first_page
            self._current_page.render(self._touchscreen.surface)
        with open('/sys/class/backlight/rpi_backlight/bl_power', 'w') as f:
            f.write(blank_str)

    def run(self, start_page, callback=None, cb_rate=None) -> NoReturn:
        """ Run the GUI, staring with the initial Page.

        Does not return, but does an exit() when done. Wrapping
        code in this thread needs to embed this in a Try/Finally to do cleanup.

        Parameters
        ----------
        start_page : Page
            The starting page to display
        callback : Callable[GUI, Page]
            An optional method to inject into the GUI main loop, for managing
            events and activities. This method SHOULD NOT take much time,
            as it is in the middle of the display loop.  Time consuming
            activities should be set up in a separate thread or process, with
            this callback doing quick actions only.
        cb_rate : Int
            The (approximate) number of milliseconds between calls to the
            callback (it helps if it's some multiple of 1/60, as the primary
            loop rate is 60 frames a second).
        """
        self._current_page = start_page
        self._first_page = start_page
        self._running = True

        self._touchscreen.run()

        fps_clock = pygame.time.Clock()

        def handle_touches(e, t):
            """ Call the `Page.touch_handler()` to process an event. """
            if self._blacked:
                # Consume touch if we are fully blacked out
                self.reset_display()
                return
            # Reset the brightness
            self.reset_display()

            new_page = self._current_page.touch_handler(e, t)
            if new_page is not None:
                self._current_page = new_page

        # All touch types go through the `Page.touch_handler()`
        for touch in self._touchscreen.touches:
            touch._on_press = handle_touches
            touch._on_release = handle_touches
            touch._on_move = handle_touches

        try:
            last_hook_ms = pygame.time.get_ticks()
            while self._running:
                # Deal with screen fade and blackout
                time = pygame.time.get_ticks()
                # deltaTime in seconds.
                delta_time = (time - self.last_event) / 1000.0
                if delta_time > self.BLACKOUT_TIME:
                    self.set_light(False)
                    self._blacked = True
                elif delta_time > self.FADE_TIME:
                    self.set_brightness(self.FADE_LEVEL)
                    self._faded = True

                # Call external hook if specified
                if callback is not None and (time - last_hook_ms) > cb_rate:
                    last_hook_ms = time
                    callback(self, self._current_page)

                # Render the current page
                self._current_page.render(self._touchscreen.surface)
                pygame.display.flip()

                # Lock it into the framerate
                fps_clock.tick(self.FPS)

        except Exception as e:
            backlog_error(e, f"Unmanaged Exception {type(e)}: {e}")
        finally:
            self.reset_display()
            LOG.info("Stopping touchscreen thread...")
            self._touchscreen.stop()

            LOG.info("Exiting GUI...")
            exit()

    def stop(self):
        """ Tell the GUI to stop running.

        This method isn't really accessible, but here for completeness.
        """
        self._running = False
