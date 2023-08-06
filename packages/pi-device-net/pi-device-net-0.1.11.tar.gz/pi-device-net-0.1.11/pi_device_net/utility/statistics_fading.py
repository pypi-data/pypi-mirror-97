# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Rudimentary online statistics, providing an approximate mean value
    of the data stream.
"""
from pi_device_net._interfaces import IStatistics


class StatisticsFading(IStatistics):
    def __init__(self, window_size, oldest_weight):
        """ Online statistics, where the older samples have less weight than
        newer samples. No samples are stored, only three internal values.

        Parameters
        ----------
        window_size : Integer
            How many samples we are representing
        oldest_weight : Float
            The relative weight of the oldest sample.  Should be a fairly
            small value.
        """
        self.reset()
        self._init(window_size, oldest_weight)

    def _init(self, window_size, oldest_weight):
        self.alpha = pow(oldest_weight, 1.0 / window_size)

    def reset(self):
        self.sum = 0.0
        self.sum2 = 0.0
        self.increment = 0.0

    def set(self, alpha, sum, sum2, increment):
        self.alpha = alpha
        self.sum = sum
        self.sum2 = sum2
        self.increment = increment

    def update(self, sample):
        self.sum = (self.alpha * self.sum) + sample
        self.increment = (self.alpha * self.increment) + 1.0

    def mean(self):
        # If we haven't gotten enough data, we return a mean of zero (to
        # avoid floating point explosions)
        if self.increment > 0.01:
            return self.sum / self.increment
        else:
            return 0.0
