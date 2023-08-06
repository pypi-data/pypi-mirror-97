FROM python:3.8.3-slim-buster

ADD requirements.txt /langauge/core/dispatcher/requirements.txt
WORKDIR /
ENV PYTHONPATH /

RUN pip3 install -r /langauge/core/dispatcher/requirements.txt

ADD . /langauge/core/dispatcher

ARG CELERY_WORKERS

RUN echo $CELERY_WORKERS

# run the worker
ENTRYPOINT celery -A langauge.core.dispatcher.task.tasks worker --loglevel=INFO --concurrency=$CELERY_WORKERS