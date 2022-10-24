import redis
from config.settings import default_settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

redis_conn = redis.Redis(
    host=default_settings.redis_host,
    port=default_settings.redis_port,
    db=0,
)

db = SQLAlchemy()


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = default_settings.postgres
    db.init_app(app)
    import storages.postgres.db_models as models

    models.init_tables(app)
