#!/bin/bash

while ! nc -z -v postgres 5432; do
      sleep 1
    done

while ! nc -z -v redis 6379; do
      sleep 1
    done

cd /auth/app/
alembic upgrade head
uwsgi --http 0.0.0.0:5000 --master -p 4 -w wsgi:app
