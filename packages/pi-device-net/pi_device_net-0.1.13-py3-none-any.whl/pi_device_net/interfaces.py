# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    PiDeviceNet interfaces (and most of the Device implementation.
"""
import logging
import threading
from abc import ABC, abstractmethod

import pygame

from constants import SAMPLE_RATE

LOG = logging.getLogger(__name__)


class IDevice(ABC):
    """ Base class for devices, giving threaded behavior to query hardware.

    There are two sides to a Device.

    Device Thread:
        The child of IDevice implements the `_read()` method .

        When the client calls `run()`, a thread is started that repeatedly
        calls the specific `_read()` and stores the result.

    Device Client:
        To start the device thread(s), call `run()`.

        To see the most recent value, check the `value` property. If an
        archiver is specified, see the most recent set of values using
        the `history()` method.

    The device also supports two optional systems:

    * IStatistics object, to perform online statistical interpretation of the
        value stream

    * IArchiver object, to provide a memory for the value stream
    """
    def __init__(self, device_name,
                 statistics=None,
                 archiver=None):
        """ Initialize the device.

        Parameters
        ----------
        device_name : String
            The name of the device, used as part of the storage scheme and
            for other references.
        statistics : IStatistics
            If specified, each value will be sent to `update()` to track
            whatever details about the device's behavior the IStatistics
            tracks (`mean()` at a minimum).
        archiver : IArchiver
            If specified, each value will be sent to 'put()'. You can query
            the archiver using IDevice `history()` method or methods on the
            archiver itself.
        """
        self.name = device_name
        self.sample_rate = None

        self._statistics = statistics
        self._archiver = archiver
        self._thread = None
        self._running = False
        self._last_reading = None

    # === Data access

    @abstractmethod
    def _read(self):
        """ Read a value from the hardware. The only abstract method in this
        interface. The child class must implement the actual device read.

        Returns
        -------
        Number
            The value that represents the current state of the device. In
            theory it doesn't have to be a number, but some of the companion
            interfaces may expect a number.
        """

    @property
    def value(self):
        """ The last read value for this device.

        Returns
        -------
        Number (or whatever this device uses as its state)
        """
        return self._last_reading

    def list_history(self, tail=None):
        """ If an archiver was specified, returns the most recent set of
        values archived.

        Parameters
        ----------
        tail : Int
            If specified, determines how many values to return (clamped to
            the buffer size).  Defaults to returning all values in memory.

        Returns
        -------
        list(Number)
            The list may be empty or have fewer entries than requested,
            depending on the state of the archiver.
        """
        if self._archiver is None:
            return []
        return self._archiver.history(tail)

    # === Execution control

    def run(self, sample_rate=None):
        """ Start the device thread, which will call `_read()` at the
        specified sample rate.

        Parameters
        ----------
        sample_rate : Int
            The time between samples in milliseconds. Defaults to 1,000 (one
            sample per second).
        """
        if self._thread is not None:
            LOG.warning("Already running")
            return

        if self._archiver is not None:
            LOG.info("Starting archiver")
            self._archiver.run()

        self.sample_rate = sample_rate or SAMPLE_RATE
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        if self._thread is None:
            LOG.warning("Already stopped")
            return

        if self._archiver is not None:
            LOG.info("Stopping archiver")
            self._archiver.stop()

        self._running = False
        self._thread.join()
        self._thread = None

    # === Utility methods

    def map_ranges(self, input, input_min, input_max,
                   output_min, output_max):
        """ Utility method to map an input between two value ranges.

        Parameters
        ----------
        input : Number
            The number we are mapping to a new range
        input_min : Number
            The minimum value that `input` can take
        input_max : Number
            The maximum value that `input` can take
        output_min : Number
            The minimum value of the new output range
        output_max : Number
            The maximum value of the new output range

        Returns
        -------
        Number
            The input value as mapped to the output range
        """
        input_range = input_max - input_min
        output_range = output_max - output_min
        normalized_value = float(input - input_min) / float(input_range)
        return output_min + (normalized_value * output_range)

    # === Internal methods

    def _run(self):
        """ The threaded run method; reads the device at the sample rate,
        updates the device's last reading, and updates the statistics and
        archiver (if specified).

        Runs until stopped.
        """
        self._running = True
        while self._running:
            # Use the pygame framerate control
            pygame.time.wait(self.sample_rate)

            self._last_reading = self._read()
            if self._statistics:
                self._statistics.update(self._last_reading)
            if self._archiver is not None:
                self._archiver.put(self._last_reading)


class IStatistics(ABC):
    """ Online statistics, for tracking the behavior of an IDevice.
    """

    @abstractmethod
    def reset(self):
        """ Zero out the statistics held so far.
        """

    @abstractmethod
    def update(self, sample):
        """ Add a sample to the ongoing statistics.

        Parameters
        ----------
        sample : Number
            A new sample value to process. Does not have to be a number,
            if the device ecosystem as a whole is not using numbers.
        """

    @abstractmethod
    def mean(self):
        """ Retrieve the mean value of the samples to date.

        Returns
        -------
        Number
            The mean value (more or less) of all updates taken to date.
        """


class IArchiver(ABC):
    """ Manage values history for an IDevice.
    """

    @abstractmethod
    def run(self):
        """ Run the archiver, if it needs to start a thread. The archiver
        may use a separate thread or process to do slow activities, such
        as writing a chunk of the history to disk.
        """

    @abstractmethod
    def stop(self):
        """ Stop the archiver, if it started a thread.
        """

    @abstractmethod
    def put(self, value):
        """ Add a value to the archive.

        Parameters
        ----------
        value : Number
            The value to store in the archive.  Could technically be anything,
            but some of the other companion interfaces assume a numerical
            value.
        """

    @abstractmethod
    def history(self, tail=None):
        """ Return the history with an optional tail size.

        Parameters
        ----------
        tail : Int
            If specified, the number of values at the end of the archive to
            return; otherwise returns the entire archive in memory.

        Returns
        -------
        tuple(Number)
        """

