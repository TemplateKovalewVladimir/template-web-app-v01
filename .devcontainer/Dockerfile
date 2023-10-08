FROM python:3.11.6-alpine3.18

# Timezone
ENV TZ=Europe/Moscow
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN apk add --update --no-cache git

COPY pyproject.toml poetry.lock* /tmp/poetry/
RUN pip install poetry --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi -C /tmp/poetry/ \
    && rm -rf /tmp/poetry/


# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true