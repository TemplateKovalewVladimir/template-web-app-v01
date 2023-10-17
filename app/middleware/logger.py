import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.utils import ColorEnum
from app.core.utils import set_color_text_console as set_color

logger = logging.getLogger(__name__)

request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    return request_id.get()


class MiddlewareLogger(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        r_uuid = str(uuid.uuid4())
        token_context_var = request_id.set(r_uuid)

        logger.info(
            set_color("Start request_id: %s", ColorEnum.BG_BLUE),
            r_uuid,
        )
        logger.info(
            set_color("%s %s", ColorEnum.BG_GREEN),
            request.method,
            request.url.path,
        )

        start_time = time.time()
        response = await call_next(request)
        process_time = str(round(time.time() - start_time, 5))
        response.headers["X-Process-Time"] = process_time

        logger.info(
            set_color("Response status code: %s", ColorEnum.BG_GREEN),
            response.status_code,
        )
        logger.info(
            set_color("Finish request_id: %s process_time: %s", ColorEnum.BG_BLUE),
            r_uuid,
            process_time,
        )

        request_id.reset(token_context_var)

        return response
