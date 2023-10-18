from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.sqlalchemy import get_session
from app.models.user import UserModel
from app.services import LoginService

logger = getLogger(__name__)

# For database
SessionDB = Annotated[Session, Depends(get_session)]


# For auth
X_API_KEY = APIKeyHeader(name="X-API-Key")
X_API_KEY_DEPENDS = Depends(X_API_KEY)
TokenAuth = Annotated[str, X_API_KEY_DEPENDS]


def current_user_depends(token: TokenAuth) -> UserModel:
    user = LoginService.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен",
        )

    logger.info("Username: %s", user.username)
    return user


CurrentUserDepends = Annotated[UserModel, Depends(current_user_depends)]
