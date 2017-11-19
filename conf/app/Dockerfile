FROM arnulfosolis/python:latest

MAINTAINER "Arnulfo Solis <arnulfojr@me.com>"

ENV PYTHONPATH="/app/src"

ENV PATH="/app/bin/:${PATH}"

ENV FLASK_APP="init.py"

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /app/src

EXPOSE 5000

ENTRYPOINT [""]

CMD ["gunicorn", "-c", "/app/conf/app/config.py", "init:application"]

