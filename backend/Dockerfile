FROM python:3.12-alpine3.18

# Timezone
ENV TZ=Europe/Moscow
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

EXPOSE 80

WORKDIR /app

RUN apk add --update --no-cache \
    python3-dev \
    build-base openldap-dev \
    krb5 krb5-conf krb5-dev
RUN  apk add postgresql16-client=16.1-r0 --update --no-cache --repository https://dl-cdn.alpinelinux.org/alpine/edge/main --allow-untruste

COPY pyproject.toml poetry.lock* /tmp/poetry/
RUN pip install poetry --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi -C /tmp/poetry/ \
    && rm -rf /tmp/poetry/

COPY . /app

RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]