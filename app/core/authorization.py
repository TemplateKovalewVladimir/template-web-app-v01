import base64

import gssapi
from fastapi import Request, status
from fastapi.responses import JSONResponse

RESPONSE_UNAUTHORIZED = JSONResponse(
    content={"status": "unauthorized"},
    headers={"WWW-Authenticate": "Negotiate"},
    status_code=status.HTTP_401_UNAUTHORIZED,
)

RESPONSE_UNAUTHORIZED123 = JSONResponse(
    content={"status": "unauthorized"},
    status_code=status.HTTP_401_UNAUTHORIZED,
)


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
            return RESPONSE_UNAUTHORIZED123
    except gssapi.exceptions.GSSError as ex123:
        print(ex123)
        return RESPONSE_UNAUTHORIZED123

    if username is None:
        print("Not username")
        return RESPONSE_UNAUTHORIZED123

    token_output_b64 = base64.b64encode(token_output).decode("utf-8")

    response = await call_next(request)
    response.headers["WWW-Authenticate"] = f"Negotiate {token_output_b64}"

    return response
