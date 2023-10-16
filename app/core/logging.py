from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from logging.handlers import (
    QueueHandler,
    QueueListener,
    SMTPHandler,
    TimedRotatingFileHandler,
)
from os import makedirs, path
from queue import Queue
from typing import override

from app.core.config import settings
from app.core.middleware import request_id


# Formatters
class CustomFormatter(Formatter):
    @override
    def format(self, record):
        record.request_id = request_id.get()
        return super(CustomFormatter, self).format(record)


VERBOSE_FORMAT = CustomFormatter(
    "%(asctime)s [%(name)s] [%(levelname)s] [%(request_id)s] %(message)s "
)

# Handler
CONSOLE_HANDLER = StreamHandler()
CONSOLE_HANDLER.setFormatter(VERBOSE_FORMAT)

makedirs(settings.get_log_folder, exist_ok=True)
FILE_HANDLER = TimedRotatingFileHandler(
    path.join(settings.get_log_folder, "api.log"),
    when="w0",
)
FILE_HANDLER.setFormatter(VERBOSE_FORMAT)


def get_mail_handler():
    hostname = settings.HOSTNAME

    # Конфигурация для почты
    config_mail = {
        "mailhost": settings.MAIL_HOST,
        "credentials": (settings.MAIL_USER, settings.MAIL_PASSWORD),
        "fromaddr": settings.MAIL_FROM,
        "toaddrs": settings.MAIL_TO.split(","),
    }

    config_mail_subject = f"{settings.MAIL_SUBJECT} [{hostname}]"

    # Handlers
    mail_info_handler = SMTPHandler(
        subject="INFO: " + config_mail_subject, **config_mail
    )
    mail_error_handler = SMTPHandler(
        subject="ERROR: " + config_mail_subject, **config_mail
    )
    mail_info_handler.setFormatter(VERBOSE_FORMAT)
    mail_error_handler.setFormatter(VERBOSE_FORMAT)

    # Get queue
    queue_mail_info = Queue(-1)  # SimpleQueue()
    queue_mail_error = Queue(-1)  # SimpleQueue()
    ql_mail_info = QueueListener(queue_mail_info, mail_info_handler)
    ql_mail_error = QueueListener(queue_mail_error, mail_error_handler)
    ql_mail_info.start()
    ql_mail_error.start()
    queue_mail_info_handler = QueueHandler(queue_mail_info)
    queue_mail_error_handler = QueueHandler(queue_mail_error)

    return queue_mail_info_handler, queue_mail_error_handler


def register_logger():
    # logger root
    logger_root = getLogger()
    logger_root.handlers.append(CONSOLE_HANDLER)
    logger_root.handlers.append(FILE_HANDLER)
    logger_root.setLevel(DEBUG)

    # logger Sqlalchemy
    logger_sqlalchemy = getLogger("sqlalchemy.engine")
    logger_sqlalchemy.setLevel(INFO)
    logger_sqlalchemy.handlers = []
