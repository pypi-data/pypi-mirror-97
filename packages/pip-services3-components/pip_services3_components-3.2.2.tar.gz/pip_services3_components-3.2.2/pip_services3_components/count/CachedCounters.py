# -*- coding: utf-8 -*-
"""
    pip_services3_components.counters.CachedCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached counters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading
import datetime

from .ICounters import ICounters
from .Counter import Counter
from .CounterType import CounterType
from .ITimingCallback import ITimingCallback
from .Timing import Timing
from pip_services3_commons.config.IReconfigurable import IReconfigurable

class CachedCounters(ICounters, IReconfigurable, ITimingCallback):
    """
    Abstract implementation of performance counters that measures and stores counters in memory.
    Child classes implement saving of the counters into various destinations.

    ### Configuration parameters ###
        - options:
            - interval:        interval in milliseconds to save current counters measurements (default: 5 mins)
            - reset_timeout:   timeout in milliseconds to reset the counters. 0 disables the reset (default: 0)
    """
    _default_interval = 300000

    _cache = None
    _updated = None
    _last_dump_time = None
    _interval = None
    _lock = None


    def __init__(self):
        """
        Creates a new CachedCounters object.
        """
        self._cache = {}
        self._updated = False
        self._last_dump_time = time.perf_counter()
        self._interval = self._default_interval
        self._lock = threading.Lock()


    def _save(self, counters):
        """
        Saves the current counters measurements.

        :param counters: current counters measurements to be saves.
        """
        raise NotImplementedError('Method from abstract implementation')


    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._interval = config.get_as_float_with_default("interval", self._interval)


    def clear(self, name):
        """
        Clears (resets) a counter specified by its name.

        :param name: a counter name to clear.
        """
        self._lock.acquire()
        try:
            del self._cache[name]
        finally:
            self._lock.release()


    def clear_all(self):
        """
        Clears (resets) all counters.
        """
        self._lock.acquire()
        try:
            self._cache = {}
            self._updated = False
        finally:
            self._lock.release()


    def dump(self):
        """
        Dumps (saves) the current values of counters.
        """
        if self._updated:
            messages = self.get_all()
            self._save(messages)

            self._lock.acquire()
            try:
                self._updated = False
                current_time = time.perf_counter() * 1000
                self._last_dump_time = current_time
            finally:
                self._lock.release()


    def _update(self):
        """
        Makes counter measurements as updated and dumps them when timeout expires.
        """
        self._updated = True
        
        current_time = time.perf_counter() * 1000
        if current_time > self._last_dump_time + self._interval:
            try:
                self.dump()
            except:
                # Todo: decide what to do
                pass


    def get_all(self):
        """
        Gets all captured counters.

        :return: a list with counters.
        """
        self._lock.acquire()
        try:
            return list(self._cache.values())
        finally:
            self._lock.release()


    def get(self, name, typ):
        """
        Gets a counter specified by its name.
        It counter does not exist or its type doesn't match the specified type
        it creates a new one.

        :param name: a counter name to retrieve.

        :param typ: a counter type.

        :return: an existing or newly created counter of the specified type.
        """
        if name is None or len(name) == 0:
            raise Exception("Counter name was not set")

        self._lock.acquire()
        try:
            counter = self._cache[name] if name in self._cache else None

            if counter is None or counter.type != typ:
                counter = Counter(name, typ)
                self._cache[name] = counter

            return counter
        finally:
            self._lock.release()


    def _calculate_stats(self, counter, value):
        if counter is None:
            raise Exception("Missing counter")

        counter.last = value
        counter.count = counter.count + 1 if not (counter.count is None) else 1
        counter.max = max(counter.max, value) if not (counter.max is None) else value
        counter.min = min(counter.min, value) if not (counter.min is None) else value
        counter.average = (float(counter.average * (counter.count - 1)) + value) / counter.count \
            if not (counter.average is None) and counter.count > 0 else value


    def begin_timing(self, name):
        """
        Begins measurement of execution time interval.
        It returns :class:`Timing <pip_services3_components.count.Timing.Timing>` object which has to be called at
        :func:`Timing.end_timing` to end the measurement and update the counter.

        :param name: a counter name of Interval type.

        :return: a :class:`Timing <pip_services3_components.count.Timing.Timing>` callback object to end timing.
        """
        return Timing(name, self)

    def end_timing(self, name, elapsed):
        """
        Ends measurement of execution elapsed time and updates specified counter.

        :param name: a counter name

        :param elapsed: execution elapsed time in milliseconds to update the counter.
        """
        counter = self.get(name, CounterType.Interval)
        self._calculate_stats(counter, elapsed)
        self._update()


    def stats(self, name, value):
        """
        Calculates min/average/max statistics based on the current and previous values.

        :param name: a counter name of Statistics type

        :param value: a value to update statistics
        """
        counter = self.get(name, CounterType.Statistics)
        self._calculate_stats(counter, value)
        self._update()


    def last(self, name, value):
        """
        Records the last calculated measurement value.
        Usually this method is used by metrics calculated externally.

        :param name: a counter name of Last type.

        :param value: a last value to record.
        """
        counter = self.get(name, CounterType.LastValue)
        counter.last = value
        self._update()


    def timestamp_now(self, name):
        """
        Records the current time as a timestamp.

        :param name: a counter name of Timestamp type.
        """
        self.timestamp(name, datetime.datetime.utcnow())


    def timestamp(self, name, value):
        """
        Records the given timestamp.

        :param name: a counter name of Timestamp type.

        :param value: a timestamp to record.
        """
        counter = self.get(name, CounterType.Timestamp)
        counter.time = value if not (value is None) else datetime.datetime.utcnow()
        self._update()


    def increment_one(self, name):
        """
        Increments counter by 1.

        :param name: a counter name of Increment type.
        """
        self.increment(name, 1)


    def increment(self, name, value):
        """
        Increments counter by given value.

        :param name: a counter name of Increment type.

        :param value: a value to add to the counter.
        """
        counter = self.get(name, CounterType.Increment)
        counter.count = counter.count + value if not (counter.count is None) else value
        self._update()
