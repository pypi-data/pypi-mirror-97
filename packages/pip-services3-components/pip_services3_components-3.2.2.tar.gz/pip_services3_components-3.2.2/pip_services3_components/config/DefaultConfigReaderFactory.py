# -*- coding: utf-8 -*-
"""
    pip_services3_components.connect.DefaultConfigReaderFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default discovery factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .MemoryConfigReader import MemoryConfigReader
from .JsonConfigReader import JsonConfigReader
from .YamlConfigReader import YamlConfigReader

from pip_services3_commons.refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultDiscoveryFactoryDescriptor = Descriptor(
    "pip-services", "factory", "config-reader", "default", "1.0"
)

MemoryConfigReaderDescriptor = Descriptor(
    "pip-services", "config-reader", "memory", "*", "1.0"
)

JsonConfigReaderDescriptor = Descriptor(
    "pip-services", "config-reader", "json", "*", "1.0"
)

YamlConfigReaderDescriptor = Descriptor(
    "pip-services", "config-reader", "yaml", "*", "1.0"
)

class DefaultConfigReaderFactory(Factory):
    """
    Creates :class:`IConfigReader <pip_services3_components.config.IConfigReader.IConfigReader>` components by their descriptors.
    """
    def __init__(self):
        """
        Create a new instance of the factory.
        """
        self.register_as_type(MemoryConfigReaderDescriptor, MemoryConfigReader)
        self.register_as_type(JsonConfigReaderDescriptor, JsonConfigReader)
        self.register_as_type(YamlConfigReaderDescriptor, YamlConfigReader)
