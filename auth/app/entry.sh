#!/bin/bash

while ! nc -z -v postgres 5432; do
      sleep 1
    done

while ! nc -z -v redis 6379; do
      sleep 1
    done

cd /auth/app/
alembic upgrade head
uwsgi --ini uwsgi.ini
