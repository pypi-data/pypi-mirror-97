# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Function registry to map function names to implementations for page
    deserialization (in case the import is not consistent from serialization
    to deserialization)
"""


class FunctionRegistry(object):
    """ Provides function import translation for de-serialization.

    A glorified dictionary for now.
    """

    def __init__(self):
        self.registry = {}

    def register(self, function):
        """ Register a function for deserialization

        Parameters
        ----------
        function : Callable
            The function that implements the name, to allow a function to
            be found separately than the original module from serialization.
        """
        name = function.__name__
        if name in self.registry:
            raise ValueError(f"The function {name!r} is already registered")
        self.registry[name] = function

    def retrieve(self, name):
        """ Retrieve the callable for the given name.

        Parameters
        ----------
        name : String
            The name associated with the callable

        Returns
        -------
        Callable
            The function that implements the name, or None
        """
        return self.registry.get(name)

    def list_names(self):
        """ List all known names.
        More useful for debugging than anything else.

        Returns
        -------
        List(String)
        """
        return sorted(self.registry)
