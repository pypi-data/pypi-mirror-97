# -*- coding: utf-8 -*-
"""
    pip_services3_components.counters.Counter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Counter object implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class Counter(object):
    """
    Data object to store measurement for a performance counter.
    This object is used by :class:`CachedCounters <pip_services3_components.count.CachedCounters.CachedCounters>` to store counters.
    """
    name = None
    type = None
    last = None
    count = None
    min = None
    max = None
    average = None
    time = None

    def __init__(self, name= None, tipe = None):
        """
        Creates a instance of the data obejct

        :param name: a counter name.

        :param tipe: a counter type.
        """
        self.name = name
        self.type = tipe
