FROM python:2.7-alpine

MAINTAINER "Arnulfo Solis <arnulfojr@me.com>"

ENV PYTHONPATH="/app/src"

ENV PATH="/app/bin/:${PATH}"

ENV FLASK_APP="init.py"

COPY . /app

WORKDIR /app

RUN apk add --no-cache build-base postgresql-libs postgresql-dev libffi-dev && \
    pip install -r requirements.txt && \
    apk del build-base

WORKDIR /app/src

EXPOSE 5000

ENTRYPOINT [""]

CMD ["gunicorn", "-c", "/app/conf/app/conf.py", "init:application"]

