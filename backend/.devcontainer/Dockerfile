FROM python:3.12-alpine3.18

# Timezone
ENV TZ=Europe/Moscow
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# git
RUN apk add --update --no-cache git

# for python-ldap
RUN apk add --update --no-cache build-base openldap-dev python3-dev
# for kerberos
RUN apk add --update --no-cache krb5 krb5-conf krb5-dev

COPY pyproject.toml poetry.lock* /tmp/poetry/
RUN pip install poetry --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi -C /tmp/poetry/ \
    && rm -rf /tmp/poetry/


# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true