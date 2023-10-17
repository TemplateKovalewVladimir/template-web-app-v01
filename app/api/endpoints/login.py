from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, HTTPBasicCredentials

from app.services import LoginService

router = APIRouter()

X_API_KEY = APIKeyHeader(name="X-API-Key")


@router.post("/token/basic/")
def get_token_basic(data: HTTPBasicCredentials):
    return {"token": data.username + data.password}


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

    # Если начинается на TlRMTVNTUAAB, то это 100% NTLM
    # Kerberos обычно начинает на YII, но не всегда!
    if token_authorization[:12] == "TlRMTVNTUAAB":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The authentication method is not supported",
        )

    username_kerberos = LoginService.authorization_kerberos(token_authorization)
    return username_kerberos


@router.get("/test")
def test(token: str = Depends(X_API_KEY)):
    return token
