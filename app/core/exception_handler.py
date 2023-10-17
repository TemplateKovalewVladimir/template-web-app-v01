from logging import getLogger

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = getLogger(__name__)


def error_response_content(request: Request, error_type: str, error_detail: str):
    # Из Request нельзя извлечь body запроса и соответственно json
    # см issues и discussions
    # https://github.com/tiangolo/fastapi/issues/1909
    # https://github.com/tiangolo/fastapi/discussions/9109

    if error_type == "Exception":
        logger.critical("!" * 100)

    error_content = jsonable_encoder(
        {
            "status": "error",
            "error": {
                "type": error_type,
                "detail": error_detail,
            },
            "request": {
                "method": request.method,
                "path": request.url.path,
                "path_params": request.path_params,
            },
        }
    )

    return error_content


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response_content(
            request=request,
            error_type="StarletteHTTPException",
            error_detail=exc.detail,
        ),
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response_content(
            request=request,
            error_type="RequestValidationError",
            error_detail=exc.errors(),
        ),
    )


async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response_content(
            request=request,
            error_type="Exception",
            error_detail=getattr(exc, "__str__", lambda: None)(),
        ),
    )
