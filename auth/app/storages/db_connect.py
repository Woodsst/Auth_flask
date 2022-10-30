from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from config.settings import default_settings

redis_conn: Optional[Redis] = None

db: Optional[SQLAlchemy] = None


def postgres_init(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = default_settings.postgres
    global db
    db = SQLAlchemy()
    db.init_app(app)


def redis_init():
    global redis_conn
    redis_conn = Redis(
        host=default_settings.redis_host,
        port=default_settings.redis_port,
        db=0,
    )
