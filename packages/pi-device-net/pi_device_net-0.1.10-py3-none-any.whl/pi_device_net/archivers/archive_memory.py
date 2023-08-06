# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Provide a value history in Memory
"""
import logging

from pi_device_net._interfaces import IArchiver

LOG = logging.getLogger(__name__)


class ArchiveMemory(IArchiver):
    """ Manage multiple readings in memory.  Uses a circular buffer to
    minimize re-allocations.
    """

    def __init__(self, size):
        """ Initialize the memory archiver.

        Parameters
        ----------
        size : Int
            The number of samples to hold in memory
        """
        self._buffer = [None] * size
        self._size = size
        self._insert = 0
        self._running = False

    def run(self):
        self._running = True

    def stop(self):
        self._running = False

    def put(self, value):
        """ Add a value to the memory archive, looping through the static
        history buffer.
        """
        if not self._running:
            raise RuntimeError("Memory archive is not running.")

        self._buffer[self._insert] = value
        self._insert = (self._insert + 1) % self._size

    @property
    def history(self, size=None):
        """ Return the history with an optional size to return.

        Slices the buffer to give a coherent result, given the circular
        nature of the buffer.

        Parameters
        ----------
        size : Int
            The number of values to return. If specified larger than the
            buffer size, will be clamped to the buffer size.

        Returns
        -------
        tuple(Number)
            A list of size `size` of the most recent values.  If enough
            samples haven't been put in to fill this size, the return may
            include trailing `None` values.
        """
        size = size or self._size
        # Clamp size to buffer size
        size = min(size, self._size)

        # Determine the sub-areas of the buffer to return...
        # ... insert point towards up to the size or buffer end
        block_a = min(self._size, self._insert + size)
        # ... start of buffer filling out the request size
        block_b = size - (block_a - self._insert)
        # Slice and dice the return!  Cast to tuple to make it immutable.
        return tuple(self._buffer[self._insert:block_a]
                     + self._buffer[0:block_b])
