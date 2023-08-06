# -*- coding: utf-8 -*-
"""
    pip_services3_components.log.CompositeLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Composite logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ILogger import ILogger
from .Logger import Logger
from pip_services3_commons.refer.Descriptor import Descriptor
from pip_services3_commons.refer.IReferenceable import IReferenceable

class CompositeLogger(Logger, IReferenceable):
    """
    Aggregates all loggers from component references under a single component.

    It allows to log messages and conveniently send them to multiple destinations.

    ### References ###
        - `*:logger:*:*:1.0` 	(optional) :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components to pass log messages

    Example:

    .. code-block:: python

        class MyComponent(IConfigurable, IReferenceable):
            _logger = CompositeLogger()

            def configure(self, config):
                self._logger.configure(config)

            def set_references(self, references):
                self._logger.set_references(references)

            def my_method(self, correlation_id):
                self._logger.debug(correlationId, "Called method mycomponent.mymethod")

    """
    _loggers = None

    def __init__(self, references = None):
        """
        Creates a new instance of the logger.

        :param references: references to locate the component dependencies.
        """
        self._loggers = []

        if not (references is None):
            self.set_references(references)
            
    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        super(CompositeLogger, self).set_references(references)
        # descriptor = Descriptor(None, "logger", None, None, None)
        loggers = references.get_optional(Descriptor(None, "logger", None, None, None))
        for logger in loggers:
            if isinstance(logger, ILogger):
                self._loggers.append(logger)

    def _write(self, level, correlation_id, error, message):
        """
        Writes a log message to the logger destination.

        :param level: a log level.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        for logger in self._loggers:
            logger.log(level, correlation_id, error, message)

