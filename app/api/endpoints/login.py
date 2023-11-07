from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials

from app.schemas.login import TokenSchema
from app.services import LoginService

router = APIRouter()


_no_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не зарегистрирован в программе",
)


@router.post("/token/basic/")
def get_token_basic(data: HTTPBasicCredentials) -> TokenSchema:
    username_ldap = LoginService.authorization_ldap(data.username, data.password)
    if username_ldap is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
        )

    token = LoginService.get_token(username_ldap)
    if token is None:
        raise _no_token_exception

    return token


@router.get("/token/sso/")
def get_token_sso(request: Request):
    # https://msdn.microsoft.com/en-us/library/ms995329.aspx
    token_authorization = request.headers.get("authorization", "")[10:]
    if token_authorization == "":
        return JSONResponse(
            content={"status": "unauthorized"},
            headers={"WWW-Authenticate": "Negotiate"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Если token начинается на TlRMTVNTUAAB, то это 100% NTLM
    # Kerberos обычно начинает на YII, но не всегда!
    if token_authorization[:12] == "TlRMTVNTUAAB":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Метод аутентификации не поддерживается",
        )

    username_kerberos = LoginService.authorization_kerberos(token_authorization)
    username = username_kerberos.partition("@")[0]

    token = LoginService.get_token(username)
    if token is None:
        raise _no_token_exception

    return token
