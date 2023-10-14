import base64
import time

import gssapi
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


RESPONSE_UNAUTHORIZED = JSONResponse(
    content={"status": "unauthorized"},
    headers={"www-authenticate": "Negotiate"},
    status_code=status.HTTP_401_UNAUTHORIZED,
)


@app.middleware("http")
async def authorization_kerberos(request: Request, call_next):
    # https://winitpro.ru/index.php/2020/07/13/sozdat-keytab-fajl-spn-kerberos-autentifikacya-ad/
    # https://habr.com/ru/articles/274931/
    # https://pc.ru/articles/vklyuchaem-sso-avtorizaciyu-kerberos-ili-ntlm-v-mozilla-firefox
    # https://github.com/COUR4G3/flask-gssapi/blob/master/flask_gssapi.py

    # /etc/krd5.conf
    # /etc/krd5.keytab

    token_authorization = request.headers.get("authorization", "")[10:]

    if token_authorization == "":
        return RESPONSE_UNAUTHORIZED

    try:
        gssapi_name = gssapi.Name("HTTP/iz2vekdev-u.aa.aliter.spb.ru@AA.ALITER.SPB.RU")
        gssapi_cred = gssapi.Credentials(name=gssapi_name, usage="accept")

        gssapi_ctx = gssapi.SecurityContext(creds=gssapi_cred, usage="accept")

        token_authorization_b64 = base64.b64decode(token_authorization)
        token_output = gssapi_ctx.step(token_authorization_b64)

        if gssapi_ctx.complete:
            print("Token validated successfully!")
            username = str(gssapi_ctx.initiator_name)
        else:
            print("Token validation failed!")
            return RESPONSE_UNAUTHORIZED
    except gssapi.exceptions.GSSError as ex123:
        print(ex123)
        return RESPONSE_UNAUTHORIZED

    if username is None:
        print("Not username")
        return RESPONSE_UNAUTHORIZED

    token_output_b64 = base64.b64encode(token_output).decode("utf-8")

    response = await call_next(request)
    response.headers["WWW-Authenticate"] = f"Negotiate {token_output_b64}"

    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
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
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
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
async def all_exception_handler(_request: Request, exc: Exception):
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
