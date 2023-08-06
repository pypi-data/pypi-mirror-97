# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Graphical User Interface objects

    A `Page` is a set of widgets that define the interaction and display
    surface of the GUI

    The `GUI` manages the hardware and runs the Pages
"""
import importlib
import json
import logging
from pathlib import Path
from typing import List, Optional

import pygame

from pi_touch_gui._utilities import backlog_error
from pi_touch_gui._widget_bases import IWidget, IWidgetInterface
from pi_touch_gui.colors import BLACK
from pi_touch_gui.widget_functions import IFunction

LOG = logging.getLogger(__name__)


class Page(object):
    LCARS = 'lcars'

    def __init__(self, name, widgets=None, background=None):
        """ A collection of widgets that make up an interaction page.

        Parameters
        ----------
        name : String
            Name of the page for internal and callback reference
        widgets : List[IWidget]
        background : str
            Background image resource filepath for this Page
        """
        # If no widgets added on init, they can be added with `add_widgets()`
        # later.
        self.name = name
        self.widgets = widgets or []

        if background == Page.LCARS:
            background = str(Path(Path(__file__).parent,
                                  "assets/lcars_screen.png"))
        self.background = background
        self._bg_image = None

        if widgets is None:
            self.widgets = []
        else:
            self.widgets = widgets
        self._widget_data = {}

        self._last_adjustment = pygame.time.get_ticks()
        self._adjustment_rate = 100

    @property
    def widget_data(self):
        # Global named data store for widgets to communicate
        return self._widget_data

    def set_background(self, filepath):
        self.background = filepath
        self._bg_image = pygame.image.load(filepath).convert()

    def add_widgets(self, widgets):
        """ Add widgets to the Page.

        Parameters
        ----------
        widgets : List[IWidget]
        """
        self.widgets += widgets

    def touch_handler(self, event, touch) -> Optional['Page']:
        """ Update all widgets with a touch event.

            The first widget to consume the touch wins, and downstream
            widgets won't be tested.

            If no widget consumes the event, we call `function(self) -> Page`

        Parameters
        ----------
        event : int
            Event code defined for the interface; e.g. _widget_bases.py imports
            TS_PRESS, TS_RELEASE, and TS_MOVE
        touch : Touch
            The Touch object for the event.

        Returns
        -------
        Optional[Page]
            If the widget function names a new page, it is returned here
        """
        # Give the widgets the page context
        touch.page = self

        for widget in self.widgets:
            consumed, new_page = widget.event(event, touch)
            if consumed:
                return new_page

        return None

    def render(self, surface: pygame.Surface):
        """Redraw all widgets to screen.

        Call `render()` for all widgets in the Page, once per frame.

        Parameters
        ----------
        surface : pygame.Surface
            Surface (screen) to draw to
        """
        # Lazy loading to avoid pygame initialization issues
        if self._bg_image is None and self.background is not None:
            self._bg_image = pygame.image.load(self.background).convert()

        if self._bg_image is not None:
            surface.blit(self._bg_image, (0, 0))
        else:
            surface.fill(BLACK)
        for widget in self.widgets:
            try:
                widget.render(self, surface)
            except Exception as e:
                backlog_error(e, f"Problem rendering widget {widget}")
                raise

    def iter_widgets(self):
        """ Iterate over the widgets in the page.

        Returns
        -------
        iter(IWidget)
        """
        return iter(self.widgets)

    def serialize(self, readable=False):
        """ Serialize this page and return it as a JSON string, suitable
        to be deserialized()

        Parameters
        ----------
        readable : Bool
            True if we return formatted json

        Returns
        -------
        String
            json representation of this Page
        """
        indent = 4 if readable else None
        functions = set()

        serial_page = json.dumps(self._do_serialize(self, functions),
                          indent=indent,
                          sort_keys=True)
        LOG.info(f"Page {self.name!r} uses:  {functions}")
        return serial_page

    def list_functions(self):
        functions = set()
        self._do_serialize(self, functions)
        return functions

    def _do_serialize(self, entity, functions=None):
        entity_type = type(entity)

        if entity is None:
            return None

        if entity_type in [str, int, float, complex, bool]:
            return entity

        elif entity_type in [list, tuple, set]:
            # JSON doesn't distinguish list-equivalent types
            return [self._do_serialize(v, functions)
                    for v in entity]

        elif entity_type is dict:
            return {k: self._do_serialize(v, functions)
                    for k, v in entity.items()}

        elif callable(entity):
            path = '.'.join([entity.__module__,
                             entity.__qualname__]).split('.')
            context = '.'.join(path[:-1])
            name = path[-1]

            if '<locals>' in context:
                raise ValueError(f'Can not serialize local function '
                                 f'{context}.{name}')
            if '<lambda>' in context:
                raise ValueError(f'Can not serialize lambda function '
                                 f'{context}.{name}')
            elif 'builtins' in context:
                raise ValueError(f'Can not serialize builtin function '
                                 f'{context}.{name}')

            if functions is not None:
                functions.add(name)
            return {'__Function': {'context': context,
                                   'name': name}}

        elif issubclass(entity_type, Page):
            return self._do_serialize_object(entity, functions)

        elif issubclass(entity_type, IWidgetInterface):
            return self._do_serialize_object(entity, functions)

        elif issubclass(entity_type, IFunction):
            return self._do_serialize_object(entity, functions)

        else:
            raise TypeError(f"Unsupported type {entity_type!r}")

    def _do_serialize_object(self, entity, functions):
        ent_type = type(entity)
        kwargs = {k: self._do_serialize(v, functions)
                  for k, v in vars(entity).items()
                  if not k.startswith('_')}
        return {'__Object': {'module': ent_type.__module__,
                             'class': ent_type.__name__,
                             'kwargs': kwargs}}

    @classmethod
    def deserialize(cls, serial, registry=None):
        """ Deserialize the data and return the Page it started as.

        Parameters
        ----------
        serial : String
            Serialized page
        registry : FunctionRegistry
            Registry of functions to replace normal imports

        Returns
        -------
        Page
        """
        data = json.loads(serial)
        return Page._do_deserialize(registry, data)
        pass

    @classmethod
    def _do_deserialize(cls, registry, entity):
        entity_type = type(entity)

        if entity is None:
            return None
        if entity_type in [str, int, float, complex, bool]:
            return entity
        if entity_type is list:
            return [Page._do_deserialize(registry, v) for v in entity]
        elif entity_type is dict:
            content = {}
            for key in entity.keys():
                if key == '__Function':
                    value = entity[key]
                    context = value['context']
                    func_name = value['name']
                    return Page._get_context(registry, context, func_name)
                elif key == '__Object':
                    value = entity[key]
                    module = value['module']
                    class_name = value['class']
                    kwargs = Page._do_deserialize(registry, value['kwargs'])
                    c = Page._get_context(registry, module, class_name)
                    return c(**kwargs)
                else:
                    content.update(
                        {key: Page._do_deserialize(registry, entity[key])})
            return content
        else:
            raise TypeError(f"Unsupported type {entity_type!r}")

    @classmethod
    def _get_context(cls, registry, module, item):
        if registry:
            function =  registry.retrieve(item)
            if function is not None:
                return function

        path = module.split('.')
        imp = path[0]
        try:
            m = importlib.import_module(imp)
        except Exception as e:
            raise ImportError(f"Unable to import {module!r}.{item}: {e}")
        for part in path[1:]:
            m = getattr(m, part)
        return getattr(m, item)
