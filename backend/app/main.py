def create_app():
    from fastapi import FastAPI
    from fastapi.exceptions import RequestValidationError
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.exceptions import HTTPException as StarletteHTTPException

    from app.api import api
    from app.core.config import settings
    from app.core.exception_handler import (
        all_exception_handler,
        http_exception_handler,
        request_validation_exception_handler,
    )
    from app.core.logging import register_logger
    from app.middleware import MiddlewareDB, MiddlewareLogger

    # Регистрирую логи
    register_logger()

    # Создаю FastAPI
    app = FastAPI(title=settings.APP_TITLE)

    # Подключаю endpoints
    app.include_router(api.api_router)

    # Подключаю middleware
    # ПОРЯДОК ДОБАВЛЕНИЯ ВАЖЕН
    app.add_middleware(MiddlewareDB)
    app.add_middleware(MiddlewareLogger)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_http_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаю обработку ошибок
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(Exception, all_exception_handler)

    return app


 

