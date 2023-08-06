# -*- coding: utf-8 -*-
"""
    pip_services3_components.config.MemoryConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.config.ConfigParams import ConfigParams
from .IConfigReader import IConfigReader
from pip_services3_commons.config.IReconfigurable import IReconfigurable

class MemoryConfigReader(IConfigReader, IReconfigurable):
    """
    Config reader that stores configuration in memory.

    ### Configuration parameters ###

        The configuration parameters are the configuration template

    Example:

    .. code-block:: python
    
        config = ConfigParams.from_tuples("connection.host", "{{SERVICE_HOST}}",
                                         "connection.port", "{{SERVICE_PORT}}{{^SERVICE_PORT}}8080{{/SERVICE_PORT}}")

        configReader = MemoryConfigReader()
        configReader.configure(config)

        parameters = ConfigParams.fromValue(os.get_env())
        configReader.readConfig("123", parameters)
    """
    _config = None

    def __init__(self, config = None):
        """
        Creates a new instance of config reader.

        :param config: (optional) component configuration parameters
        """
        self._config = config
        
    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._config = config

    #todo
    def read_config(self, correlation_id, parameters):
        """
        Reads configuration and parameterize it with given values.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: ConfigParams configuration.
        """
        return ConfigParams(self._config)

    def read_config_section(self, section):
        config = self._config.get_section(section) if self._not (config is None) else None
        return config
