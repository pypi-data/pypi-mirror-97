# -*- coding: utf-8 -*-
"""
    pip_services3_components.connect.IDicovery
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Discovery service interface
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ConnectionParams import ConnectionParams

class IDiscovery:
    """
    Interface for discovery services which are used to store and resolve connection parameters to connect to external services.
    """
    def register(self, correlation_id, key, connection):
        """
        Registers connection parameters into the discovery service.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connection parameters.

        :param connection: a connection to be registered.
        """
        raise NotImplementedError('Method from interface definition')

    def resolve_one(self, correlation_id, key):
        """
        Resolves a single connection parameters by its key.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connection.

        :return: a resolved connection.
        """
        raise NotImplementedError('Method from interface definition')

    def resolve_all(self, correlation_id, key):
        """
        Resolves all connection parameters by their key.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the connections.

        :return: a list with resolved connections.
        """
        raise NotImplementedError('Method from interface definition')
