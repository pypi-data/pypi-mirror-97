# -*- coding: utf-8 -*-
"""
    pip_services3_components.count.NullCounter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null counter implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ICounters import ICounters
from .Timing import Timing

class NullCounters(ICounters):
    """
    Dummy implementation of performance counters that doesn't do anything.
    It can be used in testing or in situations when counters is required but shall be disabled.
    """

    def begin_timing(self, name):
        """
        Begins measurement of execution time interval.
        It returns :class:`Timing <pip_services3_components.count.Timing.Timing>` object which has to be called at
        :func:`end_timing <pip_services3_components.count.Timing.Timing.end_timing>` to end the measurement and update the counter.

        :param name: a counter name of Interval type.

        :return: a :class:`Timing <pip_services3_components.count.Timing.Timing>` callback object to end timing.
        """
        return Timing()

    def stats(self, name, value):
        """
        Calculates min/average/max statistics based on the current and previous values.

        :param name: a counter name of Statistics type

        :param value: a value to update statistics
        """
        pass

    def last(self, name, value):
        """
        Records the last calculated measurement value.
        Usually this method is used by metrics calculated externally.

        :param name: a counter name of Last type.

        :param value: a last value to record.
        """
        pass

    def timestamp_now(self, name):
        """
        Records the current time as a timestamp.

        :param name: a counter name of Timestamp type.
        """
        pass

    def timestamp(self, name, value):
        """
        Records the given timestamp.

        :param name: a counter name of Timestamp type.

        :param value: a timestamp to record.
        """
        pass

    def increment_one(self, name):
        """
        Increments counter by 1.

        :param name: a counter name of Increment type.
        """
        pass

    def increment(self, name, value):
        """
        Increments counter by given value.

        :param name: a counter name of Increment type.

        :param value: a value to add to the counter.
        """
        pass
