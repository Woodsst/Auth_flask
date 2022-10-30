FROM python:3.10

COPY . auth

RUN apt-get update && apt-get install -y netcat

RUN pip install -r /auth/app/requirements.txt

WORKDIR /auth/app
