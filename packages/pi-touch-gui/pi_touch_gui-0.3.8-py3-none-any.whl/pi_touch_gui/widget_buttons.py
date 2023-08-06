# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Buttons are widgets that are pressed. They typically update their function
    on release, and the contents can be as simple as a label and as complex
    as a multivalued graph.
"""
import logging
import uuid
from typing import Tuple, Optional

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._widget_bases import (IButtonWidget, IWidgetInterface)
from pi_touch_gui.widget_functions import ButtonGroupFunction

LOG = logging.getLogger(__name__)


class Button(IButtonWidget):
    """ A simple rectangular button that calls its function on release.

    It is an empty instantiation of IButtonWidget.
    """
    # Button style
    RECTANGLE = 0
    LEFT_ROUND = 1
    RIGHT_ROUND = 2
    OBROUND = 3

    # Button behavior
    CLICK = 0
    HOLD = 1
    TOGGLE = 2

    @doc_inherit(IButtonWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 style=None,
                 behavior=None,
                 **kwargs):
        """ Initialize the Button.

        Parameters
        ----------
        style : Int
            The style in which the button is rendered (Button.RECTANGLE is the
            default, but you can also specify LEFT_ROUND, RIGHT_ROUND, or both
            with OBROUND)
        behavior : Int
            The behavior of the button (Button.CLICK is the default, activating
            on release, but you can specify HOLD which activates on press
            and stops on release, or TOGGLE which turns on and off on each
            release).
        """
        super(Button, self).__init__(position, size, **kwargs)
        self.style = style or Button.RECTANGLE
        self.behavior = behavior or Button.CLICK

    @doc_inherit(IButtonWidget.render, style='numpy_with_merge')
    def render(self, page, surface):
        """ Render the button.

        Complicated by the need for one or two rounded ends.  If you play
        your parameters right, you get a circle!
        """
        color, label_color = self.state_colors(self._active)

        radius = int(self._h / 2)
        inset_x = radius if self.style & self.LEFT_ROUND else 0
        inset_w = radius if self.style & self.RIGHT_ROUND else 0
        inset_w = inset_w + inset_x
        subrect = ((self._x + inset_x, self._y),
                   (self._w - inset_w, self._h))
        pygame.draw.rect(surface, color, subrect, 0)
        if self.style & self.LEFT_ROUND:
            pygame.draw.circle(surface, color,
                               (self._x + radius, self._y + radius),
                               radius)
        if self.style & self.RIGHT_ROUND:
            pygame.draw.circle(surface, color,
                               (self._x + self._w - radius, self._y + radius),
                               radius)

        self.render_centered_text(surface, self.label, label_color, color)

    def set(self, page):
        if self.behavior == Button.TOGGLE:
            self._active = True

            if self._function_override:
                return self._function_override.update(page, self, self._active)
            elif self.function:
                return self.function.update(page, self, self._active)

    def clear(self, page):
        if self.behavior == Button.TOGGLE:
            self._active = False

            if self._function_override:
                return self._function_override.update(page, self, self._active)
            elif self.function:
                return self.function.update(page, self, self._active)

    def _on_press(self, touch) -> None:
        """ Hold behavior calls their function on the press event.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for buttons
        """
        self.press(touch.page)

    def press(self, page):
        if self.behavior == self.HOLD:
            self._active = True

            if self._function_override:
                return self._function_override.update(page, self, self._active)
            elif self.function:
                self.function.update(page, self, self._active)
        super(Button, self).press(page)

    def _on_release(self, touch):
        return self.release(touch.page)

    def release(self, page):
        if self.behavior == self.TOGGLE:
            self._active = not self._active
        else:
            self._active = False
        return super(Button, self).release(page)


class ButtonGroup(IWidgetInterface):
    """ A group of ToggleButton where zero or one may be active.

    When a button is made active, all the remaining are
    forced to be inactive.

    It is possible for none of the buttons to be active, if you
    de-activate the active button.

    Starts with the first button in the list active.
    """

    @doc_inherit(IWidgetInterface.__init__, style='numpy_with_merge')
    def __init__(self, toggle_buttons, widget_id=None):
        """ Initialize the button group, and hook their button functions.

        Parameters
        ----------
        toggle_buttons : List[ToggleButton]
            An ordered list of ToggleButton objects, where the first button
            is active on startup.
        widget_id : str
            Optional ID for this group, if not given, gets a random uuid.
        """
        self._label = 'group'
        self.widget_id = widget_id or str(uuid.uuid4())

        self.toggle_buttons = toggle_buttons
        self._widgets = list()
        for idx, button in enumerate(toggle_buttons):
            if not isinstance(button, Button):
                raise ValueError(f"Item {idx} {type(button)!r} "
                                 f"is not a Button")
            if button.behavior != Button.TOGGLE:
                raise ValueError(f"Button {idx} is not a TOGGLE")

            # Insert the group control method into the button
            button._function_override = ButtonGroupFunction(self.group_function)
            self._widgets.append(button)

    @property
    def sub_widgets(self):
        return self._widgets

    def group_function(self, page, button, state):
        """ Enforce the group behavior; one button on, all others off.

        Parameters
        ----------
        page : Page
            Page the button is on
        button : ToggleButton
            The button that is receiving the event
        state : bool
            The state being sent to the button

        Returns
        -------
        Optional['Page']
            Returns whatever the button's function returns.  The disabled
            button results are ignored.
        """
        # If we are enabling this button, disable all other buttons
        for btn in self._widgets:
            if btn.id != button.id:
                btn._active = False
                if btn.function:
                    btn.function.update(page, btn, False)

        # Now the actual button press
        btn = next(btn for btn in self._widgets if btn.id == button.id)
        if btn.function:
            return btn.function.update(page, btn, btn._active)
        return None

    @property
    def id(self):
        return self.widget_id

    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        for button in self._widgets:
            consumed, new_page = button.event(event, touch)
            if consumed:
                return True, new_page
        return False, None

    def render(self, page, surface):
        for button in self._widgets:
            button.render(page, surface)
