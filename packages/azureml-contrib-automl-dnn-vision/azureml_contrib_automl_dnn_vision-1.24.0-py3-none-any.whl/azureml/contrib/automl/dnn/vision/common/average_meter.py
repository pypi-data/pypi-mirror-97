# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""AverageMeter class."""


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        """reset self params to zero"""
        self.val = 0
        self.sum = 0
        self.count = 0
        self.max = float('-inf')
        self.min = float('inf')

    def update(self, val, n=1):
        """Update total sum and count for the meter

        :param val: current value
        :type val: float
        :param n: Count
        :type n: int
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.max = max(self.max, val)
        self.min = min(self.min, val)

    @property
    def avg(self):
        """Get average values

        :return: Average Value
        :rtype: float
        """
        if self.count == 0:
            return self.sum
        return self.sum / self.count

    @property
    def value(self):
        """Get current values

        :return: Current Value
        :rtype: float
        """
        return self.val

    @property
    def max_val(self):
        """Get max value that was passed to this meter.

        :return: Max value
        :rtype: float
        """
        return self.max

    @property
    def min_val(self):
        """Get min value that was passed to this meter.

        :return: Min value
        :rtype: float
        """
        return self.min

    def __str__(self):
        """String representation."""
        return "count={0}|min={1:.4f}|max={2:.4f}|avg={3:.4f}".format(self.count, self.min, self.max, self.avg)

    def __repr__(self):
        """String representation."""
        return self.__str__()
