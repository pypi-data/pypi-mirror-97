# -*- coding: utf-8 -*-
"""
    pip_services3_components.cache.DefaultCacheFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default cache factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .NullCache import NullCache
from .MemoryCache import MemoryCache

from pip_services3_commons.refer.Descriptor import Descriptor
from ..build.Factory import Factory

DefaultCacheFactoryDescriptor = Descriptor(
    "pip-services", "factory", "cache", "default", "1.0"
)

NullCacheDescriptor = Descriptor(
    "pip-services", "cache", "null", "*", "1.0"
)

MemoryCacheDescriptor = Descriptor(
    "pip-services", "cache", "memory", "*", "1.0"
)

class DefaultCacheFactory(Factory):
    """
    Creates :class:`ICache <pip_services3_components.cache.ICache.ICache>` components by their descriptors.
    """
    def __init__(self):
        """
        Create a new instance of the factory.
        """
        self.register_as_type(NullCacheDescriptor, NullCache)
        self.register_as_type(MemoryCacheDescriptor, MemoryCache)
