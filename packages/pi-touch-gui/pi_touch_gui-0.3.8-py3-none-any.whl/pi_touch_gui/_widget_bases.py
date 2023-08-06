# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Widget Base Classes, providing the core functionality of the widgets.

    Widgets are single interactive elements attached to a Page.
"""
import math
import uuid
from abc import ABC, abstractmethod
from typing import Tuple, Optional

import pygame
from custom_inherit import doc_inherit
from pygame import Color

from pi_touch_gui._utilities import snapped_value_string
from pi_touch_gui.colors import WHITE, BLACK, MEDIUM_GRAY
from pi_touch_gui.multitouch.raspberrypi_ts import (TS_PRESS, TS_RELEASE,
                                                    TS_MOVE)
from pi_touch_gui.widget_functions import ButtonFunction

# Default font name - specify one here if you want something other
# than the system default.
FONT_NAME = None

# I'm hoping you can init multiple times
pygame.init()


class IWidgetInterface(ABC):
    """ The bare minimum methods to implement to be a widget.
    """

    @property
    @abstractmethod
    def id(self):
        """ The Widget ID, uniquely identifies each widget.
        """

    @property
    def sub_widgets(self):
        return None

    @abstractmethod
    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        """ Handle touch events, translating them to individual `on_*` calls.

        Parameters
        ----------
        event : int
            Event code defined for the interface; e.g. _widget_bases.py imports
            TS_PRESS, TS_RELEASE, and TS_MOVE
        touch : Touch
            The Touch representing the event, where `touch.position` is the
            (x, y) coordinate of the touch.

        Returns
        -------
        Optional[Page]
            The page to transition to, or None to stay on this page
        """

    @abstractmethod
    def render(self, page, surface):
        """ Render to the device pygame Surface.

        Parameters
        ----------
        page : Page
        surface : pygame.Surface
        """


class IWidget(IWidgetInterface, ABC):
    """ Widget base class that processes events and holds common state.

        Sub-classes can define any or all of the three event handlers:

            _on_press(Touch) -> None
            _on_release(Touch) -> Optional[Page]
            _on_move(Touch) -> None

        where:
            `Page` : If not None, jump to that page on the next frame.
    """
    # Cache fonts, no need for each widget to have their own copy
    _font_cache = dict()

    def __init__(self, position, size,
                 widget_id=None,
                 font_size=None,
                 label=None,
                 color1=None,
                 color2=None,
                 label_color1=None,
                 label_color2=None):
        """ Initialize the widget.

        Most parameters can be ignored and will pick up sensible defaults.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the widget. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the widget's rectangular extent.
            Note that in some widgets labels or indicators could fall outside
            of these extents, and other widgets may choose to re-define the
            extent to something less rectangular.
        widget_id : str
            Optional ID for this widget, if not given, gets a random uuid.
        font_size : int
            Height of the font in pixels.  If not specified, will be 1/2 the
            height of the widget.
        label : str
        color1 : Color
            Main color of the widget as a tuple of (r, g, b) or (r, g, b, a),
            or a pygame.Color; the unselected color or foreground color
        color2 : Color
            Secondary color of the widget; selected color or background color
        label_color1 : Union[Tuple[int, int, int], Tuple[int, int, int, int]]
            Main color of the label; unselected color
        label_color2 : Color
            Secondary color of the label; selected color
        """
        self.widget_id = widget_id or str(uuid.uuid4())

        self.position = position
        self._x, self._y = position

        self.size = size
        self._w, self._h = size

        # Fill in any important values not specified
        self.label = label or ""
        self.color1 = color1 or MEDIUM_GRAY
        self.color2 = color2 or WHITE
        self.label_color1 = label_color1 or WHITE
        self.label_color2 = label_color2 or BLACK

        self.font_size = font_size or int(min(self._w, self._h) >> 1)

        font_key = f"{FONT_NAME}:{self.font_size}"
        if font_key in self._font_cache:
            font = self._font_cache[font_key]
        else:
            font = pygame.font.Font(FONT_NAME, self.font_size)
            self._font_cache[font_key] = font
        self._font = font

        self._pressed = False
        self._touches = []

        # Probe for the existence of the event handlers.
        try:
            callable(self._on_press)
        except AttributeError:
            self._on_press = None
        try:
            callable(self._on_release)
        except AttributeError:
            self._on_release = None
        try:
            callable(self._on_move)
        except AttributeError:
            self._on_move = None
        try:
            callable(self._adjust)
        except AttributeError:
            self._adjust = None

    @property
    def id(self):
        return self.widget_id

    @property
    def pressed(self) -> bool:
        """ True if the widget is currently pressed.
        """
        return len(self._touches) > 0 or self._pressed

    def touch_inside(self, touch) -> bool:
        """ Test a touch against the generic widget rectangle.

        Parameters
        ----------
        touch : Touch
            The touch coordinates, where `touch.position` is a Tuple[int, int]
            of the (x, y) position of the touch.

        Returns
        -------
        bool
            True if the touch is inside the widget extents.
        """
        x, y = touch.position
        return (self._x <= x <= self._x + self._w and
                self._y <= y <= self._y + self._h)

    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        # PRESS
        # A press can only be registered when it is in the widget bounds
        if self.touch_inside(touch):
            if event == TS_PRESS and touch not in self._touches:
                self._touches.append(touch)
                if self._on_press:
                    return True, self._on_press(touch)

        # RELEASE
        # A touch can be released even when its not over a widget.
        if event == TS_RELEASE and touch in self._touches:
            self._touches.remove(touch)
            if self._on_release:
                return True, self._on_release(touch)

        # MOVE
        # Touch movement is tracked even when it's not over a widget
        if event == TS_MOVE and touch in self._touches:
            if self._on_move:
                return True, self._on_move(touch)

        # "Not Me" - report not consumed
        return False, None

    def press(self, page):
        self._pressed = True

    def release(self, page):
        self._pressed = False

    def state_colors(self, active=None) -> Tuple[Color, Color]:
        """ Return the (color, label_color) appropriate to the current state.

        Parameters
        ----------
        active : bool
            Override to force the widget to render as active.

        Returns
        -------
        Tuple[Color, Color]
            Returns a tuple of (color, label_color) where the colors can
            be a pygame.Color or (r,g,b) or (r,g,b,a) tuples.
        """
        active = self.pressed or active is True
        if active:
            color = self.color2
            label_color = self.label_color2
        else:
            color = self.color1
            label_color = self.label_color1
        return color, label_color

    def render_centered_text(self, surface, text, color, bg_color=None):
        """ Render text in the center of the widget.

        Parameters
        ----------
        surface : pygame.Surface
        text : str
        color : Color
        bg_color : Color
            If you specify the background color, it can render the text a
            bit faster because it won't use alpha for a clear background.
        """
        if text is None:
            return

        text_bmp = self._font.render(text, 1, color, bg_color)
        textpos = text_bmp.get_rect()
        textpos.centerx = self._x + (self._w / 2)
        textpos.centery = self._y + (self._h / 2)
        surface.blit(text_bmp, textpos)

    def render_left_text(self, surface, text, color, bg_color=None):
        """ Render text in the left side of the widget.

        Parameters
        ----------
        surface : pygame.Surface
        text : str
        color : Color
        bg_color : Color
            If you specify the background color, it can render the text a
            bit faster because it won't use alpha for a clear background.
        """
        if text is None:
            return

        text_bmp = self._font.render(text, 1, color, bg_color)
        textpos = text_bmp.get_rect()
        textpos.left = self._x
        textpos.centery = self._y + (self._h / 2)
        surface.blit(text_bmp, textpos)

    def render_right_text(self, surface, text, color, bg_color=None):
        """ Render text in the right side of the widget.

        Parameters
        ----------
        surface : pygame.Surface
        text : str
        color : Color
        bg_color : Color
            If you specify the background color, it can render the text a
            bit faster because it won't use alpha for a clear background.
        """
        if text is None:
            return

        text_bmp = self._font.render(text, 1, color, bg_color)
        textpos = text_bmp.get_rect()
        textpos.right = self._x + self._w - 1
        textpos.centery = self._y + (self._h / 2)
        surface.blit(text_bmp, textpos)


class IButtonWidget(IWidget):
    """ ButtonWidget base that extends IWidget for push buttons.
    """

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, function=None, **kwargs):
        """
        Parameters
        ----------
        function : ButtonFunction
            Function to call on button events, with a True/False parameter
            that is True when pressed and False when released.
            Optionally returns a new Page to change pages.
        """
        if (function is not None and
                not issubclass(function.__class__, ButtonFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"ButtonFunction.")
        self._active = False
        self.function = function
        # Override lets things like the ButtonGroup take over the function,
        # but doesn't serialize so it won't pollute the serial form
        self._function_override = None
        super(IButtonWidget, self).__init__(position, size, **kwargs)

    def _on_release(self, touch) -> Optional['Page']:
        """ Buttons always call their function on the release event.

        It has already been determined that the touch is inside the
        widget via `touch_inside()`.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for buttons

        Returns
        -------
        Page
            If specified, the new Page to go to.
        """
        return self.release(touch.page)

    def release(self, page):
        """ Trigger the button, calling its function if specified.
        """
        super(IButtonWidget, self).release(page)
        if self._function_override:
            return self._function_override.update(page, self, self._active)
        elif self.function:
            return self.function.update(page, self, self._active)

    @doc_inherit(IWidget.render, style='numpy_with_merge')
    def render(self, page, surface):
        """ Render the generic button as a filled rectangle with a label.
        """
        color, label_color = self.state_colors()

        pygame.draw.rect(surface, color, (self.position, self.size), 0)
        self.render_centered_text(surface, self.label, label_color, color)


class IControlWidget(IWidget, ABC):
    """ ControlWidget base that extends IWidget for input controls.
    """

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 min_max,
                 start_value=None,
                 snap_value=None,
                 dynamic=None,
                 **kwargs):
        """
        Parameters
        ----------
        min_max : Tuple[float, float]
            The minimum and maximum values the control might take.
        start_value : float
            The initial value the widget holds.
        snap_value : float
            A value that defines (by example) the display (snap) resolution
            of the widget's value.  E.g. 0.01, 0.1, 1.  The snap value is
            not just a display affect, but controls the resolution of the
            adjusted value of the widget itself.
        dynamic : bool
            True if the function is called each frame the control is active,
            otherwise the function is only called on release.
        """
        super(IControlWidget, self).__init__(position, size,
                                             **kwargs)

        # Constrain the snap values to usable range
        self.snap_value = snap_value or 1
        self.snap_value = 0.01 if self.snap_value < 0.01 else self.snap_value

        self.min_max = min_max
        self._min_val, self._max_val = min_max

        # Value is in 0..1, where adjusted_value is in min_val..max_val
        self._range = self._max_val - self._min_val

        if start_value is not None:
            self._adjusted_value = start_value
            self._value = self.normalize_adjusted_value(start_value)
        else:
            self._adjusted_value = min_max[0]
            self._value = self.normalize_adjusted_value(min_max[0])

        self.dynamic = dynamic or False

        # Function must be set by the child classes AFTER this init
        self.function = None

    def map_value_to_adjusted_value(self, value) -> float:
        """ Map a value in 0..1 to an interpolated value in min_val..max_val.

        Parameters
        ----------
        value : float
            Widget's internal value in 0..1

        Returns
        -------
            Widget's external value in min_val..max_val, snapped to snap_val
        """
        # map [0, 1] to [min_val, max_val] with snap
        interp_value = float(self._min_val + (self._range * value))
        return int(interp_value / self.snap_value + 0.5) * self.snap_value

    def normalize_adjusted_value(self, adjusted_value) -> float:
        """ Normalize a value in min_val..max_val to 0..1

        Parameters
        ----------
        adjusted_value : float
            Widget's external value in min_val..max_val

        Returns
        -------
        float
            Widget's internal value in 0..1
        """
        # map [min_val, max_val] to [0, 1]
        return (adjusted_value - self._min_val) / self._range

    def value_str(self) -> str:
        """ The display version of the widget's external value.

        Returns
        -------
        str
            The string version of self._adjusted_value, which is the value
            the widget represents to the outside world.
        """
        return snapped_value_string(self._adjusted_value, self.snap_value)

    def _on_move(self, touch):
        """ Controls MAY call their function on the move event.

        If the widget was determined to be dynamic, the function is called
        on each move event with a value update.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for controls
        """
        if self.dynamic is True and self.function is not None:
            return self.function.update(touch.page, self, self._adjusted_value)

    def _adjust(self, direction):
        """ Adjust the control up or down based on sign(direction)
        """
        step = math.copysign(self.snap_value, direction)
        value = self._adjusted_value + step
        if value < self._min_val:
            value = self._min_val
        elif value > self._max_val:
            value = self._max_val
        self._adjusted_value = value
        self._value = self.normalize_adjusted_value(value)

        if self.function is not None:
            return self.function.update(self, self._adjusted_value)

    def _on_release(self, touch):
        """ Controls call their function on the release event.

        It has already been determined that the touch is inside the
        widget via `touch_inside()`.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for controls
        """
        self.release(touch.page)

    def release(self, page):
        """ Trigger the button, calling its function if specified with
        the adjusted value.
        """
        if self.function is not None:
            return self.function.update(page, self, self._adjusted_value)
