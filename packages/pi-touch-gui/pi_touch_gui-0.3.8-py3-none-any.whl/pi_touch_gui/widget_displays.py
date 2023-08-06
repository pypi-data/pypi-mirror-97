# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Displays are decorative or informative widgets that are not interactive,
    but provide feedback state via a function.
"""
import logging

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._utilities import snapped_value_string
from pi_touch_gui._widget_bases import IWidget, FONT_NAME
from pi_touch_gui.widget_functions import LightFunction, IndicatorFunction, GraphFunction

LOG = logging.getLogger(__name__)


class Label(IWidget):
    """ Text Label with a fixed color and no state function.
    """
    # Label alignment
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    def __init__(self, position, size,
                 font_size=None,
                 label=None,
                 label_color1=None,
                 label_alignment=None,
                 **kwargs):
        """ Initialize the label with a subset of the Widget parameters.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the Label. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the Label's rectangular extent.
        font_size : int
            Height of the font in pixels.  If not specified, defaults to
            the Label height (size[1])
        label : str
        label_color1 : Union[Tuple[int, int, int], Tuple[int, int, int, int]]
            Color of the Label
        label_alignment : int
            Alignment of the label in the box, one of LEFT, CENTER, or RIGHT
        """
        font_size = font_size or size[1]
        self.alignment = label_alignment or Label.CENTER

        super(Label, self).__init__(position, size,
                                    font_size=font_size,
                                    label=label,
                                    label_color1=label_color1,
                                    label_color2=label_color1)

    def render(self, page, surface, label=None, active=None):
        label = label or self.label
        color, label_color = self.state_colors(active)

        if self.alignment == Label.LEFT:
            self.render_left_text(surface, label, label_color)
        elif self.alignment == Label.CENTER:
            self.render_centered_text(surface, label, label_color)
        elif self.alignment == Label.RIGHT:
            self.render_right_text(surface, label, label_color)


class Indicator(Label):
    """ Indicators are dynamic Labels, controlled by their function.
    """

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 function=None,
                 **kwargs):
        """ Initialize the Indicator.

        If color1 is None, the indicator is colored like a label, with only
        the label colors being used.

        If color1 is specified, then the indicator is set in a filled
        rectangle with the active/inactive color.

        Parameters
        ----------
        function : IndicatorFunction
            The function that defines the content and state of the indicator.
        """
        # Set up the boxing behavior and font size.
        if (function is not None
                and not issubclass(function.__class__, IndicatorFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"IndicatorFunction.")
        self.function = function

        kw_font_size = kwargs.pop('font_size', None)
        if kwargs.get('color1') is None:
            self._box = True
            font_size = kw_font_size or (size[1] >> 1)
        else:
            self._box = False
            font_size = kw_font_size or size[1]

        super(Indicator, self).__init__(position, size,
                                        font_size=font_size,
                                        **kwargs)

    def render(self, page, surface, label=None, active=None):
        if self.function:
            active, label = self.function.status(page, self, label, active)
        else:
            active, label = False, None

        color, _ = self.state_colors(active=active)

        if self._box:
            pygame.draw.rect(surface, color, (self.position, self.size), 0)

        super(Indicator, self).render(page, surface,
                                      label=label,
                                      active=active)


class Light(IWidget):
    """ Lights are circles whose color state is determined by their function.
    """

    def __init__(self, position, size, function, **kwargs):
        """ Initialize the light with a subset of the Widget parameters.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the light. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the Light's rectangular extent.  The diameter of
            the circle is given by the minimum of w,y.
        function : LightFunction
            The function returns the (ring, fill) colors
        """
        # The parent init sets convenience properties like self.x, etc
        super(Light, self).__init__(position, size)

        if (function is not None
                and not issubclass(function.__class__, LightFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"LightFunction.")
        self.function = function

        self._radius = min(size[0], size[1]) >> 1
        self._center = (self._x + self._w // 2), (self._y + self._h // 2)

    def render(self, page, surface):
        if self.function is None:
            color1 = self.color1
            color2 = self.color2
        else:
            color1, color2 = self.function.colors(page, self)
        # Fill
        pygame.draw.circle(surface, color2, self._center, self._radius, 0)
        # Outline ring
        pygame.draw.circle(surface, color1, self._center, self._radius, 2)


class Graph(IWidget):
    """ A dynamic graph.

        Dynamic content is generated by the `function`
    """
    LABEL_INSET = 5

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 min_max=None,
                 quiet=None,
                 function=None,
                 **kwargs):
        """ Initialize the graph button.

        Parameters
        ----------
        min_max : Tuple[Number, Number]
            The minimum and maximum values to scale into the graph.  If not
            specified, will calculate based on the visible data.
        quiet : Bool
            If set and True, quiets the graph (doesn't print the values)
        function : GraphFunction
            The update is called with the number of samples being requested.
            It should return `data` with that many samples or fewer.  If it
            returns fewer than 2 samples, that trace may not be rendered.
        """
        super(Graph, self).__init__(position, size, **kwargs)
        if (function is not None
                and not issubclass(function.__class__, GraphFunction)):
            raise ValueError(f"Function type {type(function)} is not a "
                             f"GraphFunction.")
        self.function = function

        self.min_max = min_max
        self.quiet = quiet
        self._initialized = False

    def render(self, page, surface):
        """ Render the graph.

        The graph width determines how many data samples we ask for.
        The graph(s) are then drawn inside of the rectangle, with the last
        values in the graph optionally data rendered as labels to the right
        (but inside) of the graph.
        """
        if not self._initialized:
            if self.function is not None:
                # Determine how many samples the update method returns, so we
                # can scale the font appropriately.
                samples = self.function.samples(page, self, 1)
                ratio_h = max(2.5, len(samples))
                self._graph_font = pygame.font.Font(
                    FONT_NAME,
                    int(self._h / ratio_h + 0.5))
            self._initialized = True

        graph_pos = (self._x, self._y)
        graph_size = (self._w, self._h)
        pygame.draw.rect(surface, self.color1, (graph_pos, graph_size), 2)

        # We can only draw the graph(s) if there is an update method
        if self.function is None:
            return

        values = self.function.samples(page, self, graph_size[0] - 2)
        if self.min_max is None:
            min_val = 9999
            max_val = -9999
            # Determine the global min/max to scale the vertical range
            for entry in values:
                data = entry["data"]
                if len(data) > 0:
                    min_val = entry.get("min", min(min_val, min(data)))
                    max_val = entry.get("min", max(max_val, max(data)))
                else:
                    min_val = 0
                    max_val = 0
        else:
            min_val = self.min_max[0]
            max_val = self.min_max[1]

        range = max_val - min_val
        # Range must be > 0 so adjust around the existing min/max
        if range < .01:
            min_val -= .01
            max_val += .01
            range = max_val - min_val

        for entry in values:
            color = entry["color"]
            data = entry["data"]

            def scale_y_value(value):
                """ Scale the value to fit the graph box."""
                inset_range = range * 1.1
                center_val = value - (range / 2.0)
                return self._y + (self._h / 2.0
                                  - ((center_val - min_val) / inset_range)
                                  * self._h)

            # Need two data points to start the graph
            if len(data) > 1:
                prev_y = scale_y_value(data[0])
                prev_x = graph_pos[0]
                for val in data:
                    x = prev_x + 1
                    y = scale_y_value(val)
                    pygame.draw.line(surface, color, (prev_x, prev_y), (x, y),
                                     2)
                    prev_x = x
                    prev_y = y

                # Render the graph trailing value
                if self.quiet is not True:
                    text = self._graph_font.render(
                        snapped_value_string(data[-1], 0.1),
                        1,
                        color)
                    textpos = text.get_rect()
                    textpos.right = (self._x + self._w) - self.LABEL_INSET
                    # The text tracks the graph line, unless it's outside the
                    # extents, then we clamp it to inside.
                    if (prev_y + textpos.h + self.LABEL_INSET) > (
                            self._y + self._h):
                        textpos.bottom = prev_y - self.LABEL_INSET
                    elif (prev_y - textpos.h - self.LABEL_INSET) < self._y:
                        textpos.top = prev_y + self.LABEL_INSET
                    else:
                        textpos.centery = prev_y
                    surface.blit(text, textpos)
