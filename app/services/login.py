import base64
from logging import getLogger

import gssapi

from app.core.config import settings
from app.services.exception import AuthorizationKerberosException

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
            logger.info("Token validated successfully! user: %s", username)
        else:
            raise AuthorizationKerberosException("Token validation failed!")
    except gssapi.exceptions.GSSError as exc:
        msg = (getattr(exc, "__str__", lambda: None)(),)
        raise AuthorizationKerberosException(msg) from exc

    if username is None:
        raise AuthorizationKerberosException("Token validated, but no username")

    return username
