# -*- coding: utf-8 -*-

import threading
import sys

from pip_services3_commons.config import ConfigParams, IConfigurable
from pip_services3_commons.errors import ApplicationException
from pip_services3_commons.random import RandomInteger
from pip_services3_commons.run import IOpenable

from .SetInterval import SetInterval


class Shutdown(IConfigurable, IOpenable):
    __interval = None
    __mode = 'exception'
    __min_timeout = 300000
    __max_timeout = 900000

    def configure(self, config: ConfigParams):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self.__mode = config.get_as_string_with_default('mode', self.__mode)
        self.__min_timeout = config.get_as_integer_with_default('min_timeout', self.__min_timeout)
        self.__max_timeout = config.get_as_integer_with_default('max_timeout', self.__max_timeout)

    def is_opened(self):
        """
        Checks if the component is opened.
        :return: true if the component has been opened and false otherwise.
        """
        return self.__interval is not None

    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: 	(optional) transaction id to trace execution through call chain.
        """
        if self.__interval is not None:
            self.__interval.stop()

        timeout = RandomInteger.next_integer(self.__min_timeout, self.__max_timeout)
        self.__interval = SetInterval(self.shutdown, timeout)

    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: 	(optional) transaction id to trace execution through call chain.
        """
        if self.__interval is not None:
            self.__interval.stop()
            self.__interval = None

    def shutdown(self):
        """
        Crashes the process using the configured crash mode.
        """
        if self.__mode == 'null' or self.__mode == 'nullpointer':
            obj = None
            obj.crash = 123
        elif self.__mode == 'zero' or self.__mode == 'dividebyzero':
            crash = 0 / 100
        elif self.__mode == 'exit' or self.__mode == 'processexit':
            sys.exit(1)
        else:
            err = ApplicationException('test', None, 'CRASH', 'Crash test exception')
            raise err
