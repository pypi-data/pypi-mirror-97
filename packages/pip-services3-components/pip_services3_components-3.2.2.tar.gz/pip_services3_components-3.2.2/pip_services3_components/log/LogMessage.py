# -*- coding: utf-8 -*-
"""
    pip_services3_components.logs.LogMessage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log message implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

class LogMessage(object):
    """
    Data object to store captured log messages. This object is used by :class:`CachedLogger <pip_services3_components.log.CachedLogger.CachedLogger>`.
    """
    time = None
    source = None
    level = None
    correlation_id = None
    error = None
    message = None

    def __init__(self, level = None, source = None, correlation_id = None, error = None, message = None):
        """
        Creates log message

        :param level: a log level.

        :param source: the source (context name)

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        self.time = datetime.datetime.utcnow()
        self.level = level
        self.source = source
        self.correlation_id = correlation_id
        self.error = error
        self.message = message
