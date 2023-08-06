# -*- coding: utf-8 -*-
"""
    pip_services3_components.build.Factory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .IFactory import IFactory
from .CreateException import CreateException

class Registration:
    def __init__(self, locator, factory):
        self.locator = locator
        self.factory = factory

    locator = None
    factory = None


class Factory(IFactory):
    """
    Basic component factory that creates components using registered types and factory functions.

    Example:

    .. code-block:: python
    
        factory = Factory()

        factory.registerAsType(Descriptor("mygroup", "mycomponent1", "default", "*", "1.0"), MyComponent1)

        factory.create(Descriptor("mygroup", "mycomponent1", "default", "name1", "1.0"))
    """
    _registrations = []

    def register(self, locator, factory):
        """
        Registers a component using a factory method.

        :param locator: a locator to identify component to be created.

        :param factory: a factory function that receives a locator and returns a created component.
        """
        if locator is None:
            raise Exception("Locator cannot be null")
        if factory is None:
            raise Exception("Factory cannot be null")

        self._registrations.append(Registration(locator, factory))

    def register_as_type(self, locator, object_factory):
        """
        Registers a component using its type (a constructor function).

        :param locator: a locator to identify component to be created.

        :param object_factory: a component type.
        """
        if locator is None:
            raise Exception("Locator cannot be null")
        if object_factory is None:
            raise Exception("Factory cannot be null")

        def factory(locator):
            return object_factory()

        self._registrations.append(Registration(locator, factory))

    def can_create(self, locator):
        """
        Checks if this factory is able to create component by given locator.

        This method searches for all registered components and returns
        a locator for component it is able to create that matches the given locator.
        If the factory is not able to create a requested component is returns null.

        :param locator: a locator to identify component to be created.

        :return: a locator for a component that the factory is able to create.
        """
        for registration in self._registrations:
            this_locator = registration.locator
            if this_locator == locator:
                return this_locator
        return None

    def create(self, locator):
        """
        Creates a component identified by given locator.

        :param locator: a locator to identify component to be created.

        :return: the created component.
        """
        for registration in self._registrations:
            this_locator = registration.locator

            if this_locator == locator:
                try:
                    return registration.factory(locator)
                except Exception as ex:
                    if isinstance(ex, CreateException):
                        raise ex
                    
                    raise CreateException(
                        None,
                        "Failed to create object for " + str(locator)
                    ).with_cause(ex)
