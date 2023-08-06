FROM python:3.8.3-slim-buster

ADD requirements.txt /langauge/core/service/requirements.txt
WORKDIR /
ENV PYTHONPATH /

RUN pip3 install -r /langauge/core/service/requirements.txt

ADD . /langauge/core/service

ENTRYPOINT ["python3"]

CMD ["/langauge/core/service/run.py"]

EXPOSE 5000