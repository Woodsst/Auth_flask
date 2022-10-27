FROM python:3.10

COPY . auth

RUN pip install -r /auth/app/requirements.txt

WORKDIR /auth/app

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--master", "-p", "4", "-w", "wsgi:app"]
