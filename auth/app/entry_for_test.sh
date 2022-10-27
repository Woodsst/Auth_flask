#!/bin/bash

cd /auth/app/
alembic upgrade head
python app.py
