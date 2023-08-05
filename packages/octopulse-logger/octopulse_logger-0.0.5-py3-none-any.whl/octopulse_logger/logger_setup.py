# import multiprocessing
# from logging.handlers import QueueHandler, QueueListener

from google.cloud.logging_v2 import Client
from google.cloud.logging_v2 import _helpers
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports.background_thread import _Worker

from pythonjsonlogger import jsonlogger
import structlog

import datetime
import json
import logging
import logging.config


timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

shared_processors = [
    # structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    timestamper,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]


def monkeypatch_google_enqueue():
    def decode_json_then_enqueue(self, record, message, **kwargs):
        try:
            info = json.loads(message)
        except json.decoder.JSONDecodeError:
            info = {"message": message}
        finally:
            info["python_logger"] = record.name

        msg = info.pop("event", info.get("message", None))
        del info['message']
        queue_entry = {
            "info": {**info, "message": msg},
            "severity": _helpers._normalize_severity(record.levelno),
            "timestamp": datetime.datetime.utcfromtimestamp(record.created),
        }
        queue_entry.update(kwargs)

        self._queue.put_nowait(queue_entry)

    _Worker.enqueue = decode_json_then_enqueue


def configure_structlog():
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_handler(logName):
    handler = CloudLoggingHandler(Client(), name=logName)
    handler.setFormatter(jsonlogger.JsonFormatter())
    return handler


def setup(log_name=None, _env='test'):
    configure_structlog()

    if log_name is None:
        try:
            import __main__
            log_name = __main__.__loader__.name.split('.')[0]
        except:
            pass

    root_logger = logging.getLogger()

    if _env != 'prod':
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(colors=(True if _env != 'prod' else False)),
            foreign_pre_chain=shared_processors
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    else:
        monkeypatch_google_enqueue()
        google_handler = get_handler(log_name)
        root_logger.addHandler(google_handler)

    # log_queue = multiprocessing.Queue()
    # queue_listener = QueueListener(log_queue, google_handler, console_handler)
    # queue_listener.start()
    # # The queue handler pushes the log records to the log queue.
    # queue_handler = QueueHandler(log_queue)

    # root_logger.addHandler(queue_handler)
    root_logger.setLevel(logging.INFO)
