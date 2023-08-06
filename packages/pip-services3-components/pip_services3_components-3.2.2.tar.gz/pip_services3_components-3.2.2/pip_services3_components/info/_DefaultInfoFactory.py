# -*- coding: utf-8 -*-
"""
    pip_services3_components.info.DefaultInfoFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default info factory implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.refer.Descriptor import Descriptor
from ..build.Factory import Factory
from .ContextInfo import ContextInfo


ContextInfoDescriptor = Descriptor("pip-services", "context-info", "default", "*", "1.0")

ContainerInfoDescriptor = Descriptor("pip-services", "container-info", "default", "*", "1.0")

class DefaultInfoFactory(Factory):
    """
    Creates information components by their descriptors.
    """
    def __init__(self):
        """
        Create a new instance of the factory.
        """
        self.register_as_type(ContextInfoDescriptor, ContextInfo)
        self.register_as_type(ContainerInfoDescriptor, ContextInfo)