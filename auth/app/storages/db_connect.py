from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from config.settings import settings

redis_conn: Optional[Redis] = None

db: Optional[SQLAlchemy] = None


def postgres_init(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.postgres
    global db
    db = SQLAlchemy()
    db.init_app(app)


def redis_init():
    global redis_conn
    redis_conn = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=0,
    )
