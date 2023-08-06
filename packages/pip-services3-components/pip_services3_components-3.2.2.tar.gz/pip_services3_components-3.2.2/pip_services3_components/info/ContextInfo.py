# -*- coding: utf-8 -*-
"""
    pip_services3_components.info.ContextInfo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Context info implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import socket
from pytz import timezone

from pip_services3_commons.config.IReconfigurable import IReconfigurable


class ContextInfo(IReconfigurable):
    """
    Context information component that provides detail information
    about execution context: container or/and process.

    Most often ContextInfo is used by logging and performance counters
    to identify source of the collected logs and metrics.

    ### Configuration parameters ###
        - name:                 the context (container or process) name
        - description:          human-readable description of the context
        - properties:           entire section of additional descriptive properties
        - ...

    Example:

    .. code-block:: python

        contextInfo = ContextInfo()
        contextInfo.configure(ConfigParams.from_tuples(
                                "name", "MyMicroservice",
                                "description", "My first microservice"))

        context.name			# Result: "MyMicroservice"
        context.contextId		# Possible result: "mylaptop"
        context.startTime		# Possible result: 2018-01-01:22:12:23.45Z
        context.uptime			# Possible result: 3454345
    """
    __name = "unknown"
    __properties = None
    __description = None
    __context_id = socket.gethostname()
    __start_time = datetime.datetime.now()
    __uptime = 0

    def __init__(self, name=None, description=None):
        """
        Creates a new instance of this context info.

        :param name: (optional) a context name.

        :param description: (optional) a human-readable description of the context.
        """
        self.__name = name or "unknown"
        self.__description = description

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self.__name = config.get_as_string_with_default("name", self.__name)
        self.__name = config.get_as_string_with_default("info.name", self.__name)

        self.__description = config.get_as_string_with_default("description", self.__description)
        self.__description = config.get_as_string_with_default("info.description", self.__description)

        self.__properties = config.get_section("properties")

    @property
    def name(self):
        """
        Gets the context name.

        :return: the context name
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        Sets the context name.

        :param name: a new name for the context.
        """
        self.__name = name if name is not None else "unknown"

    @property
    def description(self):
        """
        Gets the human-readable description of the context.

        :return: the human-readable description of the context.
        """
        return self.__description

    @description.setter
    def description(self, description):
        """
        Sets the human-readable description of the context.

        :param description: a new human readable description of the context.
        """
        self.__description = description

    @property
    def context_id(self):
        """
        Gets the unique context id. Usually it is the current host name.

        :return: the unique context id.
        """
        return self.__context_id

    @context_id.setter
    def context_id(self, context_id):
        """
        Sets the unique context id.

        :param context_id: a new unique context id.
        """
        self.__context_id = context_id

    @property
    def start_time(self):
        """
        Gets the context start time.

        :return: the context start time.
        """
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the context start time.

        :param start_time: a new context start time.
        """
        self.__start_time = start_time

    @property
    def uptime(self):
        """
        Calculates the context uptime as from the start time.

        :return: number of milliseconds from the context start time.
        """
        return self.__uptime

    @uptime.setter
    def uptime(self, uptime):
        self.__uptime = uptime

    @property
    def properties(self):
        """
        Gets context additional parameters.

        :return: a JSON object with additional context parameters.
        """
        return self.__properties

    @properties.setter
    def properties(self, properties):
        """
        Sets context additional parameters.

        :param properties: a JSON object with context additional parameters
        """
        self.__properties = properties

    @staticmethod
    def from_config(config):
        """
        Creates a new ContextInfo and sets its configuration parameters.

        :param config: configuration parameters for the new ContextInfo.

        :return: a newly created ContextInfo
        """
        value = ContextInfo()
        value.configure(config)
        return value
