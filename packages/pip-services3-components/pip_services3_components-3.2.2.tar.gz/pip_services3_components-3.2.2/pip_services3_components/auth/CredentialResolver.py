# -*- coding: utf-8 -*-
"""
    pip_services3_components.auth.CredentialResolver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Credential resolver implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .CredentialParams import CredentialParams
from pip_services3_commons.refer.Descriptor import Descriptor
from .ICredentialStore import ICredentialStore
from pip_services3_commons.config.IConfigurable import IConfigurable
from pip_services3_commons.refer.IReferenceable import IReferenceable
from pip_services3_commons.refer.ReferenceException import ReferenceException
from pip_services3_commons.errors.ApplicationException import ApplicationException

class CredentialResolver(IConfigurable, IReferenceable):
    """
    Helper class to retrieve component credentials.

    If credentials are configured to be retrieved from
    :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`, it automatically locates :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
    in component references and retrieve credentials from there using store_key parameter.

    ### Configuration parameters ###
    credential:
        - store_key:                   (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>`
        - ...                          other credential parameters
    credentials:                   alternative to credential
        - [credential params 1]:       first credential parameters
        - ...                      credential parameters for key 1
        - ...
        - [credential params N]:       Nth credential parameters
        - ...                      credential parameters for key N

    ### References ###
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials

    Example:

    .. code-block:: python

          config = ConfigParams.from_tuples("credential.user", "jdoe",
                                            "credential.pass",  "pass123")

          credentialResolver = CredentialResolver()
          credentialResolver.configure(config)
          credentialResolver.set_references(references)
          credentialResolver.lookup("123")

    """
    _credentials = None
    _references = None

    def __init__(self, config = None, references = None):
        """
        Creates a new instance of credentials resolver.

        :param config: (optional) component configuration parameters

        :param references: (optional) component references
        """
        self._credentials = []
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
        credentials = CredentialParams.many_from_config(config)
        for credential in credentials:
            self._credentials.append(credential)

    def get_all(self):
        """
        Gets all credentials configured in component configuration.

        Redirect to CredentialStores is not done at this point.
        If you need fully fleshed credential use :func:`lookup` method instead.

        :return: a list with credential parameters
        """
        return list(self._credentials)

    def add(self, connection):
        """
        Adds a new credential to component credentials

        :param connection: new credential parameters to be added
        """
        self._credentials.append(connection)

    def _lookup_in_stores(self, correlation_id, credential):
        if credential.use_credential_store() == False: return None
        
        key = credential.get_store_key()
        if self._references is None:
            return None
        
        descriptor = Descriptor("*", "credential_store", "*", "*", "*")
        components = self._references.get_optional(descriptor)
        if len(components) == 0:
            raise ReferenceException(correlation_id, "Credential store wasn't found to make lookup")
        
        # TODO: create assync 
        for component in components:
            if isinstance(component, ICredentialStore):
                resolved_credential = component.lookup(correlation_id, key)
                if not (resolved_credential is None):
                    return resolved_credential

        return None

    def lookup(self, correlation_id):
        """
        Looks up component credential parameters. If credentials are configured to be retrieved
        from Credential store it finds a :class:`ICredentialStore <pip_services3_components.auth.ICredentialStore.ICredentialStore>` and lookups credentials there.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: resolved credential parameters or None if nothing was found.
        """
        if len(self._credentials) == 0: return None
        
        # Return connection that doesn't require discovery
        for credential in self._credentials:
            if not credential.use_credential_store():
                return credential
        
        # Return connection that require discovery
        for credential in self._credentials:
            if credential.use_credential_store():
                resolved_connection = self._lookup_in_stores(correlation_id, credential)
                if not (resolved_connection is None):
                    return resolved_connection
        
        return None

