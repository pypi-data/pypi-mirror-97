# -*- coding: utf-8 -*-
"""
    pip_services3_components.log.CachedLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import socket

from .ILogger import ILogger
from .Logger import Logger
from .LogMessage import LogMessage
from pip_services3_commons.errors.ErrorDescriptionFactory import ErrorDescriptionFactory
from pip_services3_commons.config.IReconfigurable import IReconfigurable

class CachedLogger(Logger, IReconfigurable):
    """
    Abstract logger that caches captured log messages in memory and periodically dumps them.
    Child classes implement saving cached messages to their specified destinations.

    ### Configuration parameters ###
        - level:             maximum log level to capture
        - source:            source (context) name
        - options:
            - interval:        interval in milliseconds to save log messages (default: 10 seconds)
            - max_cache_size:  maximum number of messages stored in this cache (default: 100)

    ### References ###
        - `*:context-info:*:*:1.0`     (optional) :class:`ContextInfo <pip_services3_components.info.ContextInfo.ContextInfo>` to detect the context id and specify counters source
    """
    _cache = None
    _updated = None
    _last_dump_time = None
    _interval = 60000
    _lock = None


    def __init__(self):
        """
        Creates a new instance of the logger.
        """
        self._cache = []
        self._updated = False
        self._last_dump_time = time.perf_counter() * 1000
        self._lock = threading.Lock()


    def _write(self, level, correlation_id, ex, message):
        """
        Writes a log message to the logger destination.

        :param level: a log level.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param ex: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        error = ErrorDescriptionFactory.create(ex) if not (ex is None) else None
        source = socket.gethostname() # Todo: add process/module name
        log_message = LogMessage(level, source, correlation_id, error, message)
        
        self._lock.acquire()
        try:
            self._cache.append(log_message)
        finally:
            self._lock.release()

        self._update()


    def _save(self, messages):
        """
        Saves log messages from the cache.

        :param messages: a list with log messages
        """
        raise NotImplementedError('Method from abstract implementation')


    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._interval = config.get_as_float_with_default("interval", self._interval)


    def clear(self):
        """
        Clears (removes) all cached log messages.
        """
        self._lock.acquire()
        try:
            self._cache = []
            self._updated = False
        finally:
            self._lock.release()


    def dump(self):
        """
        Dumps (writes) the currently cached log messages.
        """
        if self._updated:
            self._lock.acquire()
            try:
                if not self._updated:
                    return
                
                messages = self._cache
                self._cache = []
                
                self._save(messages)

                self._updated = False
                self._last_dump_time = time.perf_counter() * 1000
            finally:
                self._lock.release()


    def _update(self):
        """
        Makes message cache as updated and dumps it when timeout expires.
        """
        self._updated = True
        
        if time.perf_counter() * 1000 > self._last_dump_time + self._interval:
            try:
                self.dump()
            except:
                # Todo: decide what to do
                pass
