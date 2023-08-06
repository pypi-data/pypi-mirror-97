# -*- coding: utf-8 -*-
"""
    pip_services3_components.connect.ConnectionResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Connection resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.config import ConfigParams

from .ConnectionParams import ConnectionParams
from .IDiscovery import IDiscovery
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.refer.IReferenceable import IReferenceable
from pip_services3_commons.refer.Descriptor import Descriptor
from pip_services3_commons.errors.ConfigException import ConfigException

class ConnectionResolver(IConfigurable, IReferenceable):
    """
    Helper class to retrieve component connections.

    If connections are configured to be retrieved from :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>`,
    it automatically locates :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` in component references
    and retrieve connections from there using discovery_key parameter.

    ### Configuration parameters ###
        - connection:
            - discovery_key:               (optional) a key to retrieve the connection from IDiscovery
            - ...                          other connection parameters
        - connections:                  alternative to connection
            - [connection params 1]:       first connection parameters
            - ...                      connection parameters for key 1
            - [connection params N]:       Nth connection parameters
            - ...                      connection parameters for key N

    ### References ###
        - `*:discovery:*:*:1.0`    (optional) IDiscovery services to resolve connections

    Example:

    .. code-block:: python

        config = ConfigParams.from_tuples("connection.host", "10.1.1.100", "connection.port", 8080)

        connectionResolver = ConnectionResolver()
        connectionResolver.configure(config)
        connectionResolver.setReferences(references)
        connectionResolver.resolve("123")
    """
    _connections = None
    _references = None

    def __init__(self, config = None, references = None):
        """
        Creates a new instance of connection resolver.

        :param config: (optional) component configuration parameters

        :param references: (optional) component references
        """
        self._connections = []
        if not (config is None):
            self.configure(config)
        if not (references is None):
            self.set_references(references)

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._references = references

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        connections = ConnectionParams.many_from_config(config)
        for connection in connections:
            self._connections.append(connection)

    def get_all(self):
        """
        Gets all connections configured in component configuration.
        Redirect to Discovery services is not done at this point.
        If you need fully fleshed connection use :func:`resolve` method instead.

        :return: a list with connection parameters
        """
        return self._connections

    def add(self, connection):
        """
        Adds a new connection to component connections

        :param connection: new connection parameters to be added
        """
        self._connections.append(connection)

    def _register_in_discovery(self, correlation_id, connection):
        if connection.use_discovery() == False: return False
        
        key = connection.get_discovery_key()
        if self._references is None:
            return False
        
        descriptor = Descriptor("*", "discovery", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if components is None:
            return False
        
        for component in components:
            if isinstance(component, IDiscovery):
                component.register(correlation_id, key, connection)
        
        return True

    def register(self, correlation_id, connection):
        """
        Registers the given connection in all referenced discovery services.
        This method can be used for dynamic service discovery.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param connection: a connection to register.
        """
        result = self._register_in_discovery(correlation_id, connection)
        
        if result:
            self._connections.append(connection)

    def _resolve_in_discovery(self, correlation_id, connection):
        if connection.use_discovery() == False: return None
        
        key = connection.get_discovery_key()
        descriptor = Descriptor("*", "discovery", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ConfigException(correlation_id, "CANNOT_RESOLVE", "Discovery wasn't found to make resolution")

        for component in components:
            if isinstance(component, IDiscovery):
                resolved_connection = component.resolve_one(correlation_id, key)
                if not (resolved_connection is None):
                    return resolved_connection
        
        return None

    def resolve(self, correlation_id):
        """
        Resolves a single component connection. If connections are configured to be retrieved
        from Discovery service it finds a :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` and resolves the connection there.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: resolved connection parameters or null if nothing was found.
        """
        if len(self._connections) == 0: return None
        
        # Return connection that doesn't require discovery
        for connection in self._connections:
            if not connection.use_discovery():
                return connection
        
        # Return connection that require discovery
        for connection in self._connections:
            if connection.use_discovery():
                resolved_connection = self._resolve_in_discovery(correlation_id, connection)
                if not (resolved_connection is None):
                    # Merge configured and new parameters
                    resolved_connection = ConnectionParams(ConfigParams.merge_configs(connection, resolved_connection))
                    return resolved_connection
        
        return None

    def _resolve_all_in_discovery(self, correlation_id, connection):
        result = []
        
        if connection.use_discovery() == False: return result
        
        key = connection.get_discovery_key()
        descriptor = Descriptor("*", "discovery", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ConfigException(correlation_id, "CANNOT_RESOLVE", "Discovery wasn't found to make resolution")

        for component in components:
            if isinstance(component, IDiscovery):
                resolved_connections = component.resolve_all(correlation_id, key)
                if not (resolved_connections is None):
                    for connection in resolved_connections:
                        result.append(connection)
        
        return result

    def resolve_all(self, correlation_id):
        """
        Resolves all component connection. If connections are configured to be retrieved
        from Discovery service it finds a :class:`IDiscovery <pip_services3_components.connect.IDiscovery.IDiscovery>` and resolves the connection there.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a list of resolved connections.
        """
        resolved = []
        to_resolve = []

        # Sort connections
        for connection in self._connections:
            if connection.use_discovery():
                to_resolve.append(connection)
            else:
                resolved.append(connection)
        
        # Resolve addresses that require that
        if len(to_resolve) > 0:
            for connection in to_resolve:
                resolved_connections = self._resolve_all_in_discovery(correlation_id, connection)
                for resolved_connection in resolved_connections:
                    # Merge configured and new parameters
                    resolved_connection = ConnectionParams(ConfigParams.merge_configs(connection, resolved_connection))
                    resolved.append(resolved_connection)
        
        return resolved
