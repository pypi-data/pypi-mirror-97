# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from .NullLock import NullLock
from .MemoryLock import MemoryLock


class DefaultLockFactory(Factory):
    """
    Creates :class:`ILock <pip_services3_components.lock.ILock.ILock>` components by their descriptors.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`, :class:`ILock <pip_services3_components.lock.ILock.ILock>`, :class:`MemoryLock <pip_services3_components.lock.MemoryLock.MemoryLock>`, :class:`NullLock <pip_services3_components.lock.NullLock.NullLock>`
    """
    descriptor = Descriptor("pip-services", "factory", "lock", "default", "1.0")
    null_lock_descriptor = Descriptor("pip-services", "lock", "null", "*", "1.0")
    memory_lock_descriptor = Descriptor("pip-services", "lock", "memory", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultLockFactory, self).__init__()
        self.register_as_type(DefaultLockFactory.null_lock_descriptor, NullLock)
        self.register_as_type(DefaultLockFactory.memory_lock_descriptor, MemoryLock)
