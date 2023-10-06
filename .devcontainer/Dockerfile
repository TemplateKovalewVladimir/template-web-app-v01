FROM python:3.11.6-alpine3.18

# Timezone
ENV TZ=Europe/Moscow
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN apk add --update --no-cache git

RUN pip install --no-cache-dir poetry

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true