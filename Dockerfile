FROM python:3.11-alpine3.17
LABEL maintainer="daniil.kulbackiy@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./entrypoint /entrypoint
COPY ./celery/beat/start /celery/start-celerybeat
COPY ./celery/worker/start /celery/start-celeryworker
COPY ./requirements.txt /requirements.txt
COPY ./app /app

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \ 
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod +x /entrypoint && \
    chmod +x /celery/start-celerybeat && \
    chmod +x /celery/start-celeryworker

ENV PATH="/py/bin:$PATH"

USER app

ENTRYPOINT ["/entrypoint"]
