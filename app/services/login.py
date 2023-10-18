import base64
from datetime import datetime, timedelta
from logging import getLogger

import gssapi
import ldap
from jose import JWTError, jwt
from pydantic import ValidationError

from app import crud
from app.core.config import settings
from app.middleware.db import get_session
from app.models.user import UserModel
from app.schemas.login import TokenPayloadSchema, TokenSchema, TokenUserPayloadSchema
from app.services.exception import (
    AuthorizationKerberosException,
    AuthorizationLDAPException,
)

logger = getLogger(__name__)


def authorization_kerberos(token_authorization: str) -> str:
    # https://winitpro.ru/index.php/2020/07/13/sozdat-keytab-fajl-spn-kerberos-autentifikacya-ad/
    # https://habr.com/ru/articles/274931/
    # https://habr.com/ru/articles/321962/
    # https://pc.ru/articles/vklyuchaem-sso-avtorizaciyu-kerberos-ili-ntlm-v-mozilla-firefox
    # https://github.com/COUR4G3/flask-gssapi/blob/master/flask_gssapi.py

    # /etc/krd5.conf
    # /etc/krd5.keytab

    try:
        gssapi_name = gssapi.Name(settings.SSO_SPN)
        gssapi_cred = gssapi.Credentials(name=gssapi_name, usage="accept")

        gssapi_ctx = gssapi.SecurityContext(creds=gssapi_cred, usage="accept")

        token_authorization_b64 = base64.b64decode(token_authorization)
        gssapi_ctx.step(token_authorization_b64)
        # Можно получить токен в ответ. Не разобрался зачем он нужен
        # token_output = gssapi_ctx.step(token_authorization_b64)
        # token_output_b64 = base64.b64encode(token_output).decode("utf-8")

        if gssapi_ctx.complete:
            username = str(gssapi_ctx.initiator_name)
            logger.info("Token kerberos validated successfully! user: %s", username)
        else:
            raise AuthorizationKerberosException("Token validation failed!")
    except gssapi.exceptions.GSSError as exc:
        msg = (getattr(exc, "__str__", lambda: None)(),)
        raise AuthorizationKerberosException(msg) from exc

    if username is None:
        raise AuthorizationKerberosException(
            "Token kerberos validated, but no username"
        )

    return username


def authorization_ldap(username: str, password: str) -> str | None:
    # Если пароль будет пустой, то except ldap.INVALID_CREDENTIALS не сработает
    if username == "":
        return None
    if password == "":
        return None
    try:
        ldap_server = settings.LDAP_SERVER
        ldap_domain = settings.LDAP_DOMAIN

        conn = ldap.initialize(ldap_server)
        conn.simple_bind_s(username + "@" + ldap_domain, password)
    # pylint: disable-next=E1101
    except ldap.INVALID_CREDENTIALS:
        return None
    # pylint: disable-next=E1101
    except ldap.LDAPError as exc:
        raise AuthorizationLDAPException("LDAPError") from exc
    finally:
        del conn

    logger.info("Credentials validated successfully! user: %s", username)
    return username


def create_access_token(data: TokenUserPayloadSchema) -> TokenSchema:
    to_encode = TokenPayloadSchema(
        create=datetime.now().timestamp(),
        exp=datetime.combine(
            datetime.today() + timedelta(days=1),
            datetime.strptime("00:00:00", "%H:%M:%S").time(),
        ).timestamp(),
        username=data.username,
    )

    encoded_jwt = jwt.encode(
        to_encode.model_dump(),
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return TokenSchema(token=encoded_jwt)


def get_token(username: str) -> TokenSchema | None:
    """Получить токен для зарегистрированного пользователя

    Args:
        username (str): Имя пользователя

    Returns:
        TokenSchema | None: Если нет токена, то это значит что пользователь не зарегистрирован в программе
    """
    db = get_session()
    user = crud.user.get_user_by_username(db, username)

    if user is None:
        return None
    return create_access_token(TokenUserPayloadSchema(username=user.username))


def get_current_user(token: str) -> UserModel | None:
    """Функция получает токен доступа и возвращает текущего пользователя, связанного с этим токеном

    Args:
        token (str): Токен доступа

    Returns:
        UserModel | None: Модель пользователя или значение None, если пользователь не найден или токен недействителен.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        payload = TokenPayloadSchema(**payload)
    except JWTError:
        return None
    except ValidationError:
        return None

    if datetime.today().timestamp() > payload.exp:
        return None

    db = get_session()
    user = crud.user.get_user_by_username(db, payload.username)
    return user
