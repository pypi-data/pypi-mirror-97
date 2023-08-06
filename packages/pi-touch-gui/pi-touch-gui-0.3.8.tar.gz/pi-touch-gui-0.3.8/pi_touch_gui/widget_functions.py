# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Classes to represent functions for widgets, craeted to hold data for
    serialization.
"""
from abc import ABC
from copy import deepcopy


class IFunction(ABC):
    """ Generic representation of a callable function, providing a layer
    of storage and indirection for serialization.
    """

    def __init__(self, function):
        """ Init the generic function with a callable.

        Parameters
        ----------
        function : Callable
        """
        self.function = function

    def execute(self, **kwargs):
        """ Execute the generic function with generic parameters.

        Parameters
        ----------
        **kwargs : Dict

        Returns
        -------
        Any
        """
        return self.function(**kwargs)


class ButtonFunction(IFunction):
    """ A representation of a function that is useful for a button.
    """

    def __init__(self, function, data=None):
        """ Initialize the button function, with optional data that will
        be serialized with the function.

        Parameters
        ----------
        function : Callable
            The function to be called when the button changes state. Will
            be called with kwargs as a dictionary, containing `page`, `button`
            and `state` plus whatever is stored in `base_kwargs`
        data : dict
            Optional dictionary entries to be passed to the button function.
        """
        self.data = data or {}
        super(ButtonFunction, self).__init__(function)

    def update(self, page, button, state):
        """ Update the button state (e.g. for push, release, etc.).

        If the update returns a Page, that page will be the new page
        rendered.

        Parameters
        ----------
        page : Page
            The page the button is on
        button : IButtonWidget
            The button object calling update
        state : Boolean
            The state of the button, True being pushed

        Returns
        -------
        Optional['Page']
        """
        kwargs = deepcopy(self.data)
        kwargs.update({'page': page, 'button': button, 'state': state})

        return self.execute(**kwargs)


class ButtonGroupFunction(ButtonFunction):
    """ A representation of a function that is useful for a button.
    """

    def __init__(self, function, data=None):
        super(ButtonGroupFunction, self).__init__(function, data)


class IControlFunction(IFunction):
    """ A representation of a function that is useful for an input control.
    """

    def __init__(self, function, data=None):
        """ Initialize the control function, with optional data that will
        be serialized with the function.

        Parameters
        ----------
        function : Callable
            The function to be called when the control changes value. Will
            be called with kwargs as a dictionary, containing `page`,
            `control` and `value` plus whatever is stored in `base_kwargs`
        data : dict
            Optional dictionary entries to be passed to the control function.
        """
        self.data = data or {}
        super(IControlFunction, self).__init__(function)

    def update(self, page, control, value):
        """ Update the control value

        Parameters
        ----------
        page : Page
            The page the control is on
        control : ControlWidget
            The button object calling update
        value : Number
            The value of the control
        """
        kwargs = deepcopy(self.data)
        kwargs.update({'page': page, 'control': control, 'value': value})

        return self.execute(**kwargs)


class DialFunction(IControlFunction):
    def __init__(self, function, data=None):
        super(DialFunction, self).__init__(function, data)


class SliderFunction(IControlFunction):
    def __init__(self, function, data=None):
        super(SliderFunction, self).__init__(function, data)


class IndicatorFunction(IFunction):
    """ A representation of a function that is useful for an indicator (an
    active label).
    """

    def __init__(self, function, data=None):
        """ Initialize the indicator function, with optional data that will
        be serialized with the function.

        Parameters
        ----------
        function : Callable
            The function to be called to retrieve the indicator status. Will
            be called with kwargs as a dictionary, containing `page`,
            `indicator`, 'label', and 'active', plus whatever is stored in
            `base_kwargs`
        data : dict
            Optional dictionary entries to be passed to the control function.
        """
        self.data = data or {}
        super(IndicatorFunction, self).__init__(function)

    def status(self, page, indicator, label, active):
        """ Retrieve the indicator status.

        Parameters
        ----------
        page : Page
            The page the indicator is on
        indicator : IndicatorWidget
            The indicator object calling status
        label : String
            The base label of the indicator
        active : Boolean
            True if the indicator is considered "active"

        Returns
        -------
        (Bool, String)
            The bool is an 'active' flag, which sets the active color
            palette if True.  The string sets the indicator label.  If it is
            None, then the indicator defaults to self.label.
        """
        kwargs = deepcopy(self.data)
        kwargs.update({'page': page,
                       'indicator': indicator,
                       'label': label,
                       'active': active})

        return self.execute(**kwargs)


class LightFunction(IFunction):
    """ A representation of a function that is useful for the display light
    """

    def __init__(self, function, data=None):
        """ Initialize the light function, with optional data that will
        be serialized with the function.

        Parameters
        ----------
        function : Callable
            The function to be called to get the light colors. Will
            be called with kwargs as a dictionary, containing `page`, `light`
            plus whatever is stored in `base_kwargs`
        data : dict
            Optional dictionary entries to be passed to the control function.
        """
        self.data = data or {}
        super(LightFunction, self).__init__(function)

    def colors(self, page, light):
        """ Retrieve the light colors.

        Parameters
        ----------
        page : Page
            The page the light is on
        light : LightWidget
            The light object calling update

        Returns
        -------
        (Color, Color)
            The (ring, fill) colors
        """
        kwargs = deepcopy(self.data)
        kwargs.update({'page': page, 'light': light})

        return self.execute(**kwargs)


class GraphFunction(IFunction):
    """ A representation of a function that is useful for an input control.
    """

    def __init__(self, function, data=None):
        """ Initialize the button function, with optional data that will
        be serialized with the function.

        Parameters
        ----------
        function : Callable
            The function to be called to request values. Will
            be called with kwargs as a dictionary, containing `page`, `graph`
            and `num` plus whatever is stored in `base_kwargs`
        data : dict
            Optional dictionary entries to be passed to the control function.
        """
        self.data = data or {}
        super(GraphFunction, self).__init__(function)

    def samples(self, page, graph, num):
        """ Retrieve some samples

        Parameters
        ----------
        page : Page
            The page the graph is on.
        graph : GraphWidget
            The button object calling update
        num : Int
            The number of samples to retrieve

        Returns
        -------
        List[Dict]
            One dictionary per trace in the graph.
            The dictionary defines the color of the trace and a list of float
            with the sample data:
                {"color": <Color>, "data": [<float>]}

        """
        kwargs = deepcopy(self.data)
        kwargs.update({'page': page, 'graph': graph, 'num': num})

        return self.execute(**kwargs)
