# -*- coding: utf-8 -*-
"""
    pip_services3_components.build.CompositeFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Composite factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from .CreateException import CreateException
from .IFactory import IFactory

class CompositeFactory(IFactory):
    """
    Aggregates multiple factories into a single factory component.
    When a new component is requested, it iterates through
    factories to locate the one able to create the requested component.

    This component is used to conveniently keep all supported factories in a single place.

    Example:

    .. code-block:: python
    
        factory = CompositeFactory()
        factory.add(new DefaultLoggerFactory())
        factory.add(new DefaultCountersFactory())

        loggerLocator = Descriptor("*", "logger", "*", "*", "1.0")
        factory.can_create(loggerLocator)  # Result: Descriptor("pip-service", "logger", "null", "default", "1.0")
        factory.create(loggerLocator)      # Result: created NullLogger
    """
    _factories = None

    def __init__(self, *factories):
        """
        Creates a new instance of the factory.

        :param factories: a list of factories to embed into this factory.
        """
        self._factories = []
        for factory in factories:
            self._factories.append(factory)


    def add(self, factory):
        """
        Adds a factory into the list of embedded factories.

        :param factory: a factory to be added.
        """
        if factory is None:
            raise Exception("Factory cannot be null")
        
        self._factories.append(factory)


    def remove(self, factory):
        """
        Removes a factory from the list of embedded factories.

        :param factory: the factory to remove.
        """
        self._factories.remove(factory)


    def can_create(self, locator):
        """
        Checks if this factory is able to create component by given locator.

        This method searches for all registered components and returns
        a locator for component it is able to create that matches the given locator.
        If the factory is not able to create a requested component is returns null.

        :param locator: a locator to identify component to be created.

        :return: a locator for a component that the factory is able to create.
        """
        if locator is None:
            raise Exception("Locator cannot be null")
        
        # Iterate from the latest factories
        for factory in reversed(self._factories):
            locator = factory.can_create(locator)
            if not (locator is None):
                return locator
        
        return None

    def create(self, locator):
        """
        Creates a component identified by given locator.

        :param locator: a locator to identify component to be created.

        :return: the created component.
        """
        if locator is None:
            raise Exception("Locator cannot be null")

        # Iterate from the latest factories
        for factory in reversed(self._factories):
            if factory.can_create(locator):
                return factory.create(locator)
        
        raise CreateException(None, "Cannot find factory for component " + locator)
