# -*- coding: utf-8 -*-
"""
    pip_services3_components.cache.MemoryCache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory cache component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading

from .ICache import ICache
from .CacheEntry import CacheEntry
from pip_services3_commons.config.IReconfigurable import IReconfigurable
from pip_services3_commons.run.ICleanable import ICleanable

class MemoryCache(ICache, IReconfigurable, ICleanable):
    """
    Cache that stores values in the process memory.

    Remember: This implementation is not suitable for synchronization of distributed processes.

    ### Configuration parameters ###
    options:
        - timeout:               default caching timeout in milliseconds (default: 1 minute)
        - max_size:              maximum number of values stored in this cache (default: 1000)

    Example:

    .. code-block:: python
    
        cache = MemoryCache()
        cache.store("123", "key1", "ABC", 0)
    """

    _default_timeout = 60000
    _default_max_size = 1000

    _cache = None
    _count = None
    _timeout = None
    _max_size = None
    _lock = None

    def __init__(self):
        """
        Creates a new instance of the cache.
        """
        self._cache = {}
        self._count = 0
        self._max_size = self._default_max_size
        self._timeout = self._default_timeout
        self._lock = threading.Lock()

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._timeout = config.get_as_long_with_default("options.timeout", self._default_timeout)
        self._max_size = config.get_as_long_with_default("options.max_size", self._default_max_size)

    def _cleanup(self):
        oldest = None
        self._count = 0
        
        # Cleanup obsolete entries and find the oldest
        for (key, entry) in self._cache.items():
            # Remove obsolete entry
            if entry.is_expired():
                self._cache.pop(key, None)
            # Count the remaining entry 
            else:
                self._count += 1
                if oldest is None or oldest.expiration > entry.expiration:
                    oldest = entry
        
        # Remove the oldest if cache size exceeded maximum
        if self._count > self._max_size and not (oldest is None):
            self._cache.pop(oldest.key, None)
            self._count -= 1

    def retrieve(self, correlation_id, key):
        """
        Retrieves cached value from the cache using its key.
        If value is missing in the cache or expired it returns None.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a unique value key.

        :return: a cached value or None if value wasn't found or timeout expired.
        """
        self._lock.acquire()
        try:
            # Cache has nothing
            if key not in self._cache:
                return None
                
            # Get entry from the cache
            entry = self._cache[key]
                    
            # Remove entry if expiration set and entry is expired
            if entry.is_expired():
                self._cache.pop(key, None)
                self._count -= 1
                return None
            
            # Update access timeout
            return entry.value
        finally:
            self._lock.release()

    def store(self, correlation_id, key, value, timeout):
        """
        Stores value in the cache with expiration time.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a unique value key.

        :param value: a value to store.

        :param timeout: expiration timeout in milliseconds.

        :return: a cached value stored in the cache.
        """
        timeout = timeout if timeout > 0 else self._default_timeout

        self._lock.acquire()
        try:
            entry = None
            if key in self._cache:
                entry = self._cache[key]

            # Shortcut to remove entry from the cache
            if value is None:
                if not (entry is None):
                    self._cache.pop(key, None)
                    self._count -= 1
                return None
            
            # Update the entry
            if not (entry is None):
                entry.set_value(value, timeout)
            # Or create a new entry 
            else:
                entry = CacheEntry(key, value, timeout)
                self._cache[key] = entry
                self._count += 1

            # Clean up the cache
            if self._max_size > 0 and self._count > self._max_size:
                self._cleanup()
            
            return value
        finally:
            self._lock.release()
    
    def remove(self, correlation_id, key):
        """
        Removes a value from the cache by its key.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a unique value key.
        """
        self._lock.acquire()
        try:
            # Get the entry
            entry = self._cache.pop(key, None)

            # Remove entry from the cache
            if not (entry is None):
                self._count -= 1
        finally:
            self._lock.release()
    
    def clear(self, correlation_id):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._lock.acquire()
        try:
            self._cache = {}
        finally:
            self._lock.release()
    