#!/bin/bash

cd /auth/app/
alembic upgrade head
python3 main.py
