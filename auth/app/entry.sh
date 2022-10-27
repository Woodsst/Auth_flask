#!/bin/bash

cd /auth/app/
alembic upgrade head
uwsgi --http 0.0.0.0:5000 --master -p 4 -w wsgi:app
