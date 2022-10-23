import json

import jwt_api as jwt
from config.settings import default_settings
from flask import Request
from services.service_base import ServiceBase
from storages.postgres.alchemy_init import db
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis
from storages.redis.redis_connect import redis_conn
from werkzeug.security import generate_password_hash


class Registration(ServiceBase):
    def registration(self, request: Request):
        user_data = json.loads(request.data)
        user_data["device"] = request.environ.get("HTTP_USER_AGENT")
        user_data["user"]["password"] = generate_password_hash(
            user_data["user"]["password"]
        )
        payload = self.db.set_user(user_data)
        if not payload:
            return
        access = jwt.encode_access_token(payload)
        refresh = jwt.encode_refresh_token(payload)

        self.cash.set_token(
            key=f"refresh_{payload['id']}",
            value=refresh,
            expire=default_settings.JWT_refresh_time,
        )

        self.cash.set_token(
            key=f"access_{payload['id']}",
            value=access,
            expire=default_settings.JWT_access_time,
        )

        return {"access-token": access, "refresh-token": refresh}


def registration_api():
    return Registration(Postgres(db), Redis(redis_conn()))
