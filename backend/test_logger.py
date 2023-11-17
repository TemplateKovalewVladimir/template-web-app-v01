import logging
from typing import override


class CustomFormatter(logging.Formatter):
    @override
    def format(self, record):
        record.username = "1234123"
        return super(CustomFormatter, self).format(record)


VERBOSE_FORMAT = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
VERBOSE_FORMAT_ERROR = CustomFormatter(  # logging.Formatter(
    "%(asctime)s [%(name)s] [%(levelname)s] [%(username)s] %(message)s "
)


console_handler = logging.StreamHandler()
console_handler.setFormatter(VERBOSE_FORMAT)

console_handler1 = logging.StreamHandler()
console_handler1.setLevel(logging.ERROR)
console_handler1.setFormatter(VERBOSE_FORMAT_ERROR)


logger_root = logging.getLogger()
logger_root.handlers.append(console_handler)
logger_root.handlers.append(console_handler1)
logger_root.setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)


def get_user_name():
    return "123"


logging.LoggerAdapter(logging.getLogger(__name__), {"username": get_user_name()})


logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")

logger.error("Houston, we have a %s", "major problem")

logger.critical("critical")
