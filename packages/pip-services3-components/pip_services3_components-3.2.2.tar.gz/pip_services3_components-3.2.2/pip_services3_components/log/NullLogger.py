# -*- coding: utf-8 -*-
"""
    pip_services3_components.log.NullLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .LogLevel import LogLevel
from .ILogger import ILogger

class NullLogger(ILogger):
    """
    Dummy implementation of logger that doesn't do anything.
    It can be used in testing or in situations when logger is required but shall be disabled.
    """
    def get_level(self):
        """
        Gets the maximum log level. Messages with higher log level are filtered out.

        :return: the maximum log level.
        """
        return LogLevel.Nothing

    def set_level(self, level):
        """
        Set the maximum log level.

        :param level: a new maximum log level.
        """
        pass

    def log(self, level, correlation_id, error, message, *args, **kwargs):
        """
        Logs a message at specified log level.

        :param level: a log level.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def fatal(self, correlation_id, error, message, *args, **kwargs):
        """
        Logs fatal (unrecoverable) message that caused the process to crash.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def error(self, correlation_id, error, message, *args, **kwargs):
        """
        Logs recoverable application error.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def warn(self, correlation_id, message, *args, **kwargs):
        """
        Logs a warning that may or may not have a negative impact.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def info(self, correlation_id, message, *args, **kwargs):
        """
        Logs an important information message

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def debug(self, correlation_id, message, *args, **kwargs):
        """
        Logs a high-level debug information for troubleshooting.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def trace(self, correlation_id, message, *args, **kwargs):
        """
        Logs a low-level debug information for troubleshooting.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

