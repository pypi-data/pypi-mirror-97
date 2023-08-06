# Copyright (c) 2021 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Provide threaded data archival to a File (in addition to Memory)
"""
import json
import logging
import logging.handlers
from datetime import datetime
from multiprocessing import Process, Queue
from pathlib import Path
from time import time_ns

from archivers.archive_memory import ArchiveMemory

LOG = logging.getLogger(__name__)

NS_PER_MS = 1000000
SECOND = 1000
HOUR = 60 * 60 * SECOND


class ArchiveFile(ArchiveMemory):
    """ Manage multiple readings in memory while storing them also to disk
    in a separate thread.

    Also provides a memory archiver.

    Note that the memory archiver holds _every sample_ given to it, and has
    no sense of resolution or sample buckets.  The file archiver, however,
    does partition the samples based on time taken, into bins defined by
    the resolution of the archiver.

    This means that you will get different values looking at the in-memory
    `history()` and looking at the file contents.
    """

    def __init__(self,
                 data_path,
                 root_name,
                 resolution=None,
                 null_value=None,
                 accumulate=None):
        """ Initialize the file archiver.

        File archives are stored in an hourly hierarchy:

            `<data_path>/<root_name>-<year>-<month>-<day>/H<hour>`

        Parameters
        ----------
        data_path : Path
            Where the archive is to be stored
        root_name : String
            The name of this archive (typically the device name), to be
            incorporated into the archive filename.
        resolution : Int
            The bucket size of the archive, specified in milliseconds. The
            default is to store a value for each second of operation. Do
            not make this value too small or you will consume all of the
            memory!  Make it as large as possible for your reporting.
        null_value : Any
            The value to initialize the memory buffer with.  Defaults to None.
        accumulate : Boolean
            If True, then if we get more than one sample per resolution
            period, these samples are added together. Defaults to having
            the most recent sample stored in the resolution bucker.
            Examples of `accumulate=True` would be for flow counters where
            the total flow should be accumulated; a counter example is for
            a thermometer where adding the values for a bucket wouldn't make
            sense.
        """
        self._resolution = resolution or SECOND
        self._size = HOUR // self._resolution

        # Initialize the Memory archive
        super(ArchiveFile, self).__init__(self._size)

        self._data_path = data_path
        self._root_name = root_name
        self._null_value = null_value
        self._accumulate = accumulate or False
        self._thread = None
        self._write_queue = None
        self._write_proc = None

    def run(self):
        """ Start the archive writer
        """
        if self._running:
            LOG.warning("Already running")
            return

        # We communicate to the actual file writer via a multiprocessing
        # Queue.
        self._write_queue = Queue()
        self._write_proc = Process(target=_archive_writer,
                                   args=(self._write_queue,
                                         self._data_path,
                                         self._root_name,
                                         self._resolution,
                                         self._null_value,
                                         self._accumulate))

        # Start the memory archive
        super(ArchiveFile, self).run()

    def stop(self):
        """ Stop the archive writer
        """
        if not self._running:
            LOG.warning("Already stopped")
            return

        self._write_proc.terminate()
        self._write_proc.join()

        # Stop the memory archive
        super(ArchiveFile, self).stop()

    def put(self, value):
        """ Add a value to the archive.  Also pushes the value with a
        timestamp to the write queue.
        """
        if not self._running:
            raise RuntimeError("Memory archive is not running.")

        # Store the value in the memory buffer
        super(ArchiveFile, self).put(value)

        # Send the file and timestamp to the file writer. This does mean
        # that we have two memory buffers holding this value, so be sure
        # to keep the resolution sensible.
        now = time_ns() // NS_PER_MS
        self._write_queue.put((value, now))


def _archive_writer(queue,
                    data_path,
                    root_name,
                    resolution,
                    null_value,
                    accumulate):
    """ The archive writer is a separate process that manages disk output,
    separating this slow activity from the real-time constrained file
    archiver process.

    Parameters
    ----------
    queue : Queue
        (value, timestamp) data are pushed to this queue, and received here
    data_path : Path
        Where the archive is to be stored
    root_name : String
        The name of this archive (typically the device name), to be
        incorporated into the archive filename.
    resolution : Int
        The bucket size of the archive, specified in milliseconds.
    null_value : Any
        The value to initialize the memory buffer with.
    accumulate : Boolean
        If True, then if we get more than one sample per resolution
        period, these samples are added together.
    """
    # We log to a rotating file
    LOG = logging.getLogger('archive_writer')
    handler = logging.handlers.RotatingFileHandler(
        Path(data_path, f'{root_name}_archive_writer.log'),
        maxBytes=1024 * 1024,
        backupCount=3)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] "
                                           "[%(name)s.%(lineno)d] %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S"))
    handler.setLevel(logging.INFO)
    LOG.addHandler(handler)
    LOG.setLevel(logging.INFO)

    # Create the file in-memory buffer
    size = HOUR // resolution
    buffer = [null_value] * size

    # Make our base folder
    folder = Path(data_path)
    folder.mkdir(parents=True, exist_ok=True)

    LOG.info("Starting archive writer")

    # Start up time-bin tracking
    prev_when = time_ns() // NS_PER_MS
    prev_bin = (prev_when // resolution) % size
    try:
        while True:
            # Determine current bin
            value, when = queue.get()
            bin = (when // resolution) % size

            # If we have looped our buffer, write it out to disk
            if bin < prev_bin:
                date = datetime.fromtimestamp(when // 1000)
                folder = Path(data_path,
                              f'{root_name}-'
                              f'{date.year:04}.{date.month:02}.{date.day:02}')
                folder.mkdir(parents=True, exist_ok=True)
                file = Path(folder, f'H{date.hour}')
                LOG.info(f"Writing {file}")

                # Inefficient, but saving as a json list
                data_str = json.dumps(buffer)
                try:
                    with open(file, 'w') as f:
                        f.write(data_str)
                except Exception as e:
                    LOG.error(f"ERROR WRITING:  {type(e)}: {e}")

                # Reset the buffer
                buffer = [null_value] * size

            elif bin == prev_bin:
                # Accumulate or overwrite if we are in the same bin as before
                if accumulate:
                    value = buffer[bin] + value
                buffer[bin] = value

            else:
                # bin > prev_bin; new bin!  Write to it and shift prev_bin
                buffer[bin] = value
                prev_bin = bin

    except Exception as e:
        LOG.info(f"Caught exception {type(e)}: {e}")
        LOG.info("Exiting")
