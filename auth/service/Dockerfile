FROM python:3.10

COPY . app

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["uwsgi", "--http", "127.0.0.1:5000", "--master", "-p", "4", "-w", "main:app"]
