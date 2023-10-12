from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import api
from app.view import router

app = FastAPI(title="Test")


app.include_router(router)

app.include_router(api.api_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "status": "error",
                "handler": "StarletteHTTPException",
                "detail": exc.detail,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "status": "error",
                "detail": exc.errors(),
                "body": exc.body,
            }
        ),
    )


@app.exception_handler(Exception)
async def custom_http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "status": "error",
                "handler": "Exception",
                "error_message": getattr(exc, "message", None),
                "error_description": getattr(exc, "description", None),
                "error_srt": getattr(exc, "__str__", lambda: None)(),
            }
        ),
    )
