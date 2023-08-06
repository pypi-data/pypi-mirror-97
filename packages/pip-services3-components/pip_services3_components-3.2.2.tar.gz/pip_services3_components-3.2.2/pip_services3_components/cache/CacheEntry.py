# -*- coding: utf-8 -*-
"""
    pip_services3_components.cache.CacheEntry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cache entry implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

class CacheEntry(object):
    """
    Data object to store cached values with their keys used by :class:`MemoryCache <pip_services3_components.cache.MemoryCache.MemoryCache>`
    """
    expiration = None
    key = None
    value = None

    def __init__(self, key, value, timeout):
        """
        Creates a new instance of the cache entry and assigns its values.

        :param key: a unique key to locate the value.

        :param value: a value to be stored.

        :param timeout: expiration timeout in milliseconds.
        """
        self.key = key
        self.value = value
        self.expiration = time.perf_counter() * 1000 + timeout

    def set_value(self, value, timeout):
        """
        Sets a new value and extends its expiration.

        :param value: a new cached value.

        :param timeout: a expiration timeout in milliseconds.
        """
        self.value = value
        self.expiration = time.perf_counter() * 1000 + timeout

    def is_expired(self):
        """
        Checks if this value already expired.

        :return: true if the value already expires and false otherwise.
        """
        return self.expiration < time.perf_counter() * 1000
