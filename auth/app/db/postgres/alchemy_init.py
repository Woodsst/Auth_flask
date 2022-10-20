from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.settings import default_settings

db = SQLAlchemy()


def init_db(app: Flask):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = default_settings.postgres
    db.init_app(app)
    app.app_context().push()
    db.create_all()
