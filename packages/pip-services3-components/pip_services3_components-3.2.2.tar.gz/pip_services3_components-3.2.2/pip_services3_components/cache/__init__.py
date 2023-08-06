# -*- coding: utf-8 -*-
"""
    pip_services3_components.cache.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract implementation of various distributed caches. We can save an object
    to cache and retrieve it object by its key, using various implementations.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [
    'ICache', 'CacheEntry', 'NullCache',
    'MemoryCache', 'DefaultCacheFactory'
]

from .ICache import ICache
from .CacheEntry import CacheEntry
from .NullCache import NullCache
from .MemoryCache import MemoryCache
from .DefaultCacheFactory import DefaultCacheFactory