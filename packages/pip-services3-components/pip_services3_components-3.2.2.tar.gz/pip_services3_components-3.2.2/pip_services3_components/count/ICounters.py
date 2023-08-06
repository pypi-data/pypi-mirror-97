# -*- coding: utf-8 -*-
"""
    pip_services3_components.counters.ICounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for performance counters components.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class ICounters:
    """
    Interface for performance counters that measure execution metrics.
    The performance counters measure how code is performing:
    how fast or slow, how many transactions performed, how many objects
    are stored, what was the latest transaction time and so on.

    They are critical to monitor and improve performance, scalability and reliability of code in production.
    """

    def begin_timing(self, name):
        """
        Begins measurement of execution time interval.
        It returns :class:`Timing <pip_services3_components.count.Timing.Timing>` object which has to be called at
        :func:`Timing.end_timing` to end the measurement and update the counter.

        :param name: a counter name of Interval type.

        :return: a :class:`Timing <pip_services3_components.count.Timing.Timing>` callback object to end timing.
        """
        raise NotImplementedError('Method from interface definition')

    def stats(self, name, value):
        """
        Calculates min/average/max statistics based on the current and previous values.

        :param name: a counter name of Statistics type

        :param value: a value to update statistics
        """
        raise NotImplementedError('Method from interface definition')

    def last(self, name, value):
        """
        Records the last calculated measurement value.
        Usually this method is used by metrics calculated externally.

        :param name: a counter name of Last type.

        :param value: a last value to record.
        """
        raise NotImplementedError('Method from interface definition')

    def timestamp_now(self, name):
        """
        Records the current time as a timestamp.

        :param name: a counter name of Timestamp type.
        """
        raise NotImplementedError('Method from interface definition')

    def timestamp(self, name, value):
        """
        Records the given timestamp.

        :param name: a counter name of Timestamp type.

        :param value: a timestamp to record.
        """
        raise NotImplementedError('Method from interface definition')

    def increment_one(self, name):
        """
        Increments counter by 1.

        :param name: a counter name of Increment type.
        """
        raise NotImplementedError('Method from interface definition')

    def increment(self, name, value):
        """
        Increments counter by given value.

        :param name: a counter name of Increment type.

        :param value: a value to add to the counter.
        """
        raise NotImplementedError('Method from interface definition')
