# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Controls are widgets that are manipulated and return a value. They may
    update their function on move and release.
"""
import logging
import math

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._widget_bases import IControlWidget
from pi_touch_gui.widget_functions import DialFunction, SliderFunction

LOG = logging.getLogger(__name__)


class Dial(IControlWidget):
    """ Circular input control dial.
    """

    @doc_inherit(IControlWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, function, **kwargs):
        """ Initialize the dial.

        Parameters
        ----------
        function : DialFunction
            Function to call on dial events, with a new value for the
            dial.
        """
        # Dials don't use label, so block it
        if kwargs.get('label'):
            raise ValueError("Dials don't use their value as the label.")

        if (function is not None
                and not issubclass(function.__class__, DialFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"DialFunction.")

        self.size = size
        diameter = min(size[0], size[1])
        radius = diameter >> 1
        kw_font_size = kwargs.pop('font_size', None)
        font_size = kw_font_size or (radius >> 1)

        # The parent init sets convenience properties like self.x, etc
        super(Dial, self).__init__(position, (diameter, diameter),
                                   font_size=font_size,
                                   **kwargs)
        self.function = function
        self._radius = radius
        self._cx, self._cy = (self._x + self._w // 2), (self._y + self._h // 2)
        self._initialized = False

    def touch_inside(self, touch):
        """ The interior of the dial is determined by a circle.
        """
        x, y = touch.position
        distance = math.hypot(x - self._cx, y - self._cy)
        if distance <= self._radius:
            return True

        return False

    def _on_move(self, touch):
        # If too many touches, we bail
        if len(self._touches) > 1:
            return

        dx = touch._x - self._cx
        dy = touch._y - self._cy

        # Value is from 0.0 to 1.0 (percent of range)
        self._value = (math.atan2(dy, dx) % math.tau) / math.tau
        self._adjusted_value = self.map_value_to_adjusted_value(self._value)

        super(Dial, self)._on_move(touch)

    def render(self, page, surface):
        if not self._initialized:
            self.release(page)
            self._initialized = True

        wedge_rect = (self._x, self._y, self._w, self._h)
        handle_pos = (
            int(self._cx + (self._radius * math.cos(self._value * math.tau))),
            int(self._cy + (self._radius * math.sin(self._value * math.tau))))

        center = (self._cx, self._cy)
        # Draw the filled overall dial
        pygame.draw.circle(surface, self.color1, center, self._radius, 0)
        # Draw the active pie-wedge
        pygame.draw.arc(surface, self.color2, wedge_rect,
                        -self._value * math.tau, 0.0,
                        int(self._radius * 0.5))
        # Draw the handle line
        pygame.draw.line(surface, self.label_color1, center, handle_pos,
                         3)
        # Draw the handle circle
        pygame.draw.circle(surface, self.label_color1, handle_pos,
                           int(self._radius * 0.1), 0)

        self.render_centered_text(surface, self.value_str(),
                                  self.label_color1, self.color1)


class Slider(IControlWidget):
    """ Variable value input linear slider
    """

    @doc_inherit(IControlWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, function, **kwargs):
        """ Initialize the slider.

        color1 is the slider background fill
        color2 is the slider outline and active value fill
        label_color1 is the slider line (and label)

        Parameters
        ----------
        function : SliderFunction
            Function to call on slider events, with a new value for the
            dial.
        """
        # Sliders don't use label, so block it
        if kwargs.get('label'):
            raise ValueError("Dials don't use their value as the label.")

        if (function is not None
                and not issubclass(function.__class__, SliderFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"SliderFunction.")

        super(Slider, self).__init__(position, size, **kwargs)
        self.function = function
        self._initialized = False

    def _on_move(self, touch):
        # If too many touches, bail
        if len(self._touches) > 1:
            return

        x, y = touch.position

        # Compute X/Y relative to the slider
        x -= self._x
        y -= self._y

        # Check our ratios...
        if self._w > self._h:
            # Horizontal Slider
            if 0 <= x <= self._w:
                self._value = float(x) / float(self._w)

        elif self._h > self._w:
            # Vertical Slider
            if 0 <= y <= self._h:
                self._value = (self._h - float(y)) / float(self._h)

        self._adjusted_value = self.map_value_to_adjusted_value(self._value)

        super(Slider, self)._on_move(touch)

    def render(self, page, surface):
        if not self._initialized:
            self.release(page)
            self._initialized = True

        pygame.draw.rect(surface, self.color1, (self.position, self.size), 0)

        if self._w > self._h:
            # Horizontal slider
            value_w = int(self._w * self._value)
            value_x = self._x + value_w
            pygame.draw.rect(surface, self.color2,
                             ((self._x, self._y), (value_w, self._h)))
            pygame.draw.line(surface, self.label_color1,
                             (value_x, self._y), (value_x, self._y + self._h),
                             3)

        elif self._h > self._w:
            # Vertical slider
            value_h = int(self._h * self._value)
            value_y = self._y + (self._h - value_h)
            pygame.draw.rect(surface, self.color2,
                             ((self._x, value_y), (self._w, value_h)))
            pygame.draw.line(surface, self.label_color1,
                             (self._x, value_y), (self._x + self._w, value_y),
                             3)

        pygame.draw.rect(surface, self.color2, (self.position, self.size),
                         3)

        self.render_centered_text(surface, self.value_str(), self.label_color1)
