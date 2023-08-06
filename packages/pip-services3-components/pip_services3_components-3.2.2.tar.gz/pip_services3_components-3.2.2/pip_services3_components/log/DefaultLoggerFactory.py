# -*- coding: utf-8 -*-
"""
    pip_services3_components.log.DefaultLoggerFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default logger factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .NullLogger import NullLogger
from .ConsoleLogger import ConsoleLogger
from .CompositeLogger import CompositeLogger

from pip_services3_commons.refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultLoggerFactoryDescriptor = Descriptor(
    "pip-services", "factory", "logger", "default", "1.0"
)

NullLoggerDescriptor = Descriptor(
    "pip-services", "logger", "null", "*", "1.0"
)

ConsoleLoggerDescriptor = Descriptor(
    "pip-services", "logger", "console", "*", "1.0"
)

CompositeLoggerDescriptor = Descriptor(
    "pip-services", "logger", "composite", "*", "1.0"
)

class DefaultLoggerFactory(Factory):
    """
    Creates :class:`ILogger <pip_services3_components.log.ILogger.ILogger>` components by their descriptors.
    """
    def __init__(self):
        """
        Create a new instance of the factory.
        """
        self.register_as_type(NullLoggerDescriptor, NullLogger)
        self.register_as_type(ConsoleLoggerDescriptor, ConsoleLogger)
        self.register_as_type(CompositeLoggerDescriptor, CompositeLogger)
