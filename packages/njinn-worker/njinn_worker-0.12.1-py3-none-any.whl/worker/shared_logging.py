"""
Consolidated logging for the multi threaded njinn worker
"""
import logging
import logging.handlers
import multiprocessing
import zlib
from threading import Thread
from time import sleep

__memory_handler = None
shared_handler = logging.NullHandler()


class __TaskFormatterEmulation:
    def __init__(self):
        self.formatter = logging.Formatter(
            "[%(asctime)s %(levelname)s/%(threadName)s] %(task_info)s %(message)s"
        )

    def format(self, record):
        if "task_name" in record.__dict__:
            task_name = record.__dict__["task_name"]
            task_id = record.__dict__.get("task_id", "???")
            record.__dict__.setdefault(
                "task_info", f" {task_name}[{task_id}]:",
            )
        else:
            record.__dict__.setdefault("task_info", "")
        return self.formatter.format(record)


class __NjinnApiLogHandler(logging.Handler):
    def __init__(self, njinn_api, worker_name, level=logging.NOTSET):
        super().__init__(level=level)
        self.njinn_api = njinn_api
        self.worker_name = worker_name
        self.lines = []
        self.min_successful_lines = None

    def handle_logging_exception(self, e):
        print(e)

    def flush(self):
        try:
            if self.min_successful_lines is not None:
                attempted_length = self.min_successful_lines
            else:
                attempted_length = len(self.lines)
            initial_attempted_length = attempted_length
            while self.lines:
                lines = self.lines[:attempted_length]
                r = self.njinn_api.put(
                    f"/api/v1/workercom/worker_log_page/{self.worker_name}",
                    zlib.compress("\n".join(lines).encode("utf-8")),
                    headers={
                        "Content-Type": "text/plain; charset=utf-8",
                        "Content-Encoding": "gzip",
                    },
                )
                if r.status_code == 413:
                    if attempted_length == 1:
                        # single line too long, try with next one
                        self.lines = list(self.lines[1:])
                        continue
                    else:
                        attempted_length = attempted_length // 2
                else:
                    self.lines = list(self.lines[attempted_length:])
            if attempted_length < initial_attempted_length:
                self.min_successful_lines = attempted_length
        except Exception as e:
            self.handle_logging_exception(e)

    def emit(self, record):
        self.lines.append(self.format(record))


class __FlushTargetMemoryHandler(logging.handlers.MemoryHandler):
    """
    Like MemoryHandler, but flushes target when flush() is called.
    """

    def __init__(self, capacity, queue, *args, **kwargs):

        super().__init__(capacity, *args, **kwargs)
        self.queue = queue
        self.listener = None

    def flush(self):
        super().flush()
        if self.target is not None and hasattr(self.target, "flush"):
            self.target.flush()

    def start(self):
        self.listener = logging.handlers.QueueListener(self.queue, self)
        self.listener.start()

        def flush_soon():
            # flush when listener is very likely to have
            # forwarded existing messages
            sleep(5)
            self.flush()

        Thread(target=flush_soon).start()

    def close(self):
        if self.listener is not None:
            self.listener.stop()
        super().close()

    def stop(self):
        # ensure graceful listener queue shutdown
        if self.listener is not None:
            self.listener.enqueue_sentinel()


def initialize():
    global __memory_handler
    global shared_handler
    assert __memory_handler is None
    queue = multiprocessing.Queue()
    shared_handler = logging.handlers.QueueHandler(queue)
    __memory_handler = __FlushTargetMemoryHandler(500, queue)


def start(njinn_api, worker_name, level=logging.NOTSET):
    global __memory_handler
    assert __memory_handler is not None
    handler = __NjinnApiLogHandler(njinn_api, worker_name, level=level)
    handler.setFormatter(__TaskFormatterEmulation())
    __memory_handler.setTarget(handler)
    __memory_handler.start()


def stop(*args, **kwargs):
    global __memory_handler
    if __memory_handler is not None:
        __memory_handler.stop()


def flush():
    global __memory_handler
    __memory_handler.flush()


def set_level(level):
    global shared_handler
    __memory_handler.setLevel(level)
    shared_handler.setLevel(level)
