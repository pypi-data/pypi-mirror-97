'''
Patching google cloud logging
'''

import os

import google.cloud.logging

'''
The below code is modified from https://github.com/googleapis/python-logging/blob/2b5f9e3920ecf0842e7284c28fad4beb9dc6c6a4/google/cloud/logging_v2/handlers/transports/background_thread.py#L22-L36
'''
import atexit
import datetime
import logging
import sys
import threading
import time

from six.moves import queue

from google.cloud.logging_v2 import _helpers
from google.cloud.logging_v2.handlers.transports.base import Transport

_DEFAULT_GRACE_PERIOD = float(os.getenv('DCYD_MPM_GRACE_PERIOD', 10.0))  # Seconds
_DEFAULT_MAX_BATCH_SIZE = int(os.getenv('DCYD_MPM_MAX_BATCH_SIZE', 100))
_DEFAULT_MAX_LATENCY = float(os.getenv('DCYD_MPM_MAX_LATENCY', 0.1))  # Seconds


'''
The below code is modified from https://github.com/googleapis/python-logging/blob/2b5f9e3920ecf0842e7284c28fad4beb9dc6c6a4/google/cloud/logging_v2/handlers/transports/background_thread.py#L72-L103
'''
class _Worker(google.cloud.logging.handlers.transports.background_thread._Worker):
    """A background thread that writes batches of log entries."""

    def __init__(
        self,
        cloud_logger,
        *,
        grace_period=_DEFAULT_GRACE_PERIOD,
        max_batch_size=_DEFAULT_MAX_BATCH_SIZE,
        max_latency=_DEFAULT_MAX_LATENCY,
    ):
        """
        Args:
            cloud_logger (logging_v2.logger.Logger):
                The logger to send entries to.
            grace_period (Optional[float]): The amount of time to wait for pending logs to
                be submitted when the process is shutting down.
            max_batch (Optional[int]): The maximum number of items to send at a time
                in the background thread.
            max_latency (Optional[float]): The amount of time to wait for new logs before
                sending a new batch. It is strongly recommended to keep this smaller
                than the grace_period. This means this is effectively the longest
                amount of time the background thread will hold onto log entries
                before sending them to the server.
        """
        self._cloud_logger = cloud_logger
        self._grace_period = grace_period
        self._max_batch_size = max_batch_size
        self._max_latency = max_latency
        self._queue = queue.Queue(0)
        self._operational_lock = threading.Lock()
        self._thread = None

    def enqueue(self, record, message, **kwargs):
        """
        Patching enqueue function to remove the "message" wrap and "python_logger"
        Modified from https://github.com/googleapis/python-logging/blob/2b5f9e3920ecf0842e7284c28fad4beb9dc6c6a4/google/cloud/logging_v2/handlers/transports/background_thread.py#L225-L240
        """
        queue_entry = {
            "info": message if isinstance(message, dict) else {"message": message, "python_logger": record.name},
            "severity": _helpers._normalize_severity(record.levelno),
            "timestamp": datetime.datetime.utcfromtimestamp(record.created),
        }
        queue_entry.update(kwargs)
        self._queue.put_nowait(queue_entry)


'''
The below code is copied from https://github.com/googleapis/python-logging/blob/2b5f9e3920ecf0842e7284c28fad4beb9dc6c6a4/google/cloud/logging_v2/handlers/transports/background_thread.py#L247-L297

The purpose is to use the redefined _Worker class from above
'''

class BackgroundThreadTransport(Transport):
    """Asynchronous transport that uses a background thread."""

    def __init__(
        self,
        client,
        name,
        *,
        grace_period=_DEFAULT_GRACE_PERIOD,
        batch_size=_DEFAULT_MAX_BATCH_SIZE,
        max_latency=_DEFAULT_MAX_LATENCY,
    ):
        """
        Args:
            client (~logging_v2.client.Client):
                The Logging client.
            name (str): The name of the lgoger.
            grace_period (Optional[float]): The amount of time to wait for pending logs to
                be submitted when the process is shutting down.
            batch_size (Optional[int]): The maximum number of items to send at a time in the
                background thread.
            max_latency (Optional[float]): The amount of time to wait for new logs before
                sending a new batch. It is strongly recommended to keep this smaller
                than the grace_period. This means this is effectively the longest
                amount of time the background thread will hold onto log entries
                before sending them to the server.
        """
        self.client = client
        logger = self.client.logger(name)
        self.worker = _Worker(
            logger,
            grace_period=grace_period,
            max_batch_size=batch_size,
            max_latency=max_latency,
        )
        self.worker.start()

    def send(self, record, message, **kwargs):
        """Overrides Transport.send().
        Args:
            record (logging.LogRecord): Python log record that the handler was called with.
            message (str): The message from the ``LogRecord`` after being
                formatted by the associated log formatters.
            kwargs: Additional optional arguments for the logger
        """
        self.worker.enqueue(record, message, **kwargs)

    def flush(self):
        """Submit any pending log records."""
        self.worker.flush()
