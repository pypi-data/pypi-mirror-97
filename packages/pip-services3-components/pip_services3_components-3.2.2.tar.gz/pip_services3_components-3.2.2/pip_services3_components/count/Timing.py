# -*- coding: utf-8 -*-
"""
    pip_services3_components.counters.Timing
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Timing implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time

class Timing:
    """
    Callback object returned by :func:`pip_services3_components.count.ICounters.ICounters.begin_timing` to end timing
    of execution block and update the associated counter.

    Example:
        timing = counters.begin_timing("mymethod.exec_time")
        # do something
        timing.end_timing()
    """

    _start = None
    _callback = None
    _counter = None

    def __init__(self, counter = None, callback = None):
        """
        Creates a new instance of the timing callback object.

        :param counter: an associated counter name

        :param callback: a callback that shall be called when end_timing is called.
        """

        self._counter = counter
        self._callback = callback
        self._start = time.perf_counter() * 1000

    def end_timing(self):
        """
        Ends timing of an execution block, calculates elapsed time and updates the associated counter.
        """

        if not (self._callback is None):
            elapsed = time.perf_counter() * 1000 - self._start
            self._callback.end_timing(self._counter, elapsed)