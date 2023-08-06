# -*- coding: utf-8 -*-
"""
    pip_services3_components.auth.MemoryCredentialStore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory credential store implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.config.ConfigParams import ConfigParams
from pip_services3_commons.config.IReconfigurable import IReconfigurable
from pip_services3_commons.data.StringValueMap import StringValueMap
from .ICredentialStore import ICredentialStore
from .CredentialParams import CredentialParams

class MemoryCredentialStore(ICredentialStore, IReconfigurable):
    """
    Credential store that keeps credentials in memory.

    ### Configuration parameters ###
        - [credential key 1]:
        - ...                          credential parameters for key 1
        - [credential key 2]:
        - ...                          credential parameters for key N
        - ...

    Example:

    .. code-block:: python
    
        config = ConfigParams.from_tuples("key1.user", "jdoe",
                                          "key1.pass", "pass123",
                                          "key2.user", "bsmith",
                                          "key2.pass", "mypass")

        credentialStore = MemoryCredentialStore()
        credentialStore.read_credentials(config)
        credentialStore.lookup("123", "key1")
    """
    _items = None

    def __init__(self, credentials = None):
        """
        Creates a new instance of the credential store.

        :param credentials: (optional) configuration with credential parameters.
        """
        self._items = StringValueMap()
        if not (credentials is None):
            self.configure(credentials)

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self.read_credentials(config)

    def read_credentials(self, credentials):
        """
        Reads credentials from configuration parameters.
        Each section represents an individual CredentialParams

        :param credentials: configuration parameters to be read
        """
        self._items.clear()
        for key in credentials.get_key_names():
            value = credentials.get_as_nullable_string(key)
            self._items.append(CredentialParams.from_tuples([key, value]))

    def store(self, correlation_id, key, credential):
        """
        Stores credential parameters into the store.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the credential parameters.

        :param credential: a credential parameters to be stored.
        """
        if not (credential is None):
            self._items.put(key, credential)
        else:
            self._items.remove(key)

    def lookup(self, correlation_id, key):
        """
        Lookups credential parameters by its key.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the credential.

        :return: found credential parameters or None if nothing was found
        """
        credential = self._items.get_as_object(key)
