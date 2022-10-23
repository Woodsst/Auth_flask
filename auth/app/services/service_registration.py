import json

from flask import Request
from services.service_base import ServiceBase
from storages.postgres.alchemy_init import db
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis
from storages.redis.redis_connect import redis_conn
from werkzeug.security import generate_password_hash


class Registration(ServiceBase):
    def registration(self, request: Request) -> dict:
        """Регистрация нового пользователя"""

        user_data = json.loads(request.data)
        user_data["device"] = request.environ.get("HTTP_USER_AGENT")
        user_data["user"]["password"] = generate_password_hash(
            user_data["user"]["password"]
        )

        payload = self.db.set_user(user_data)
        if not payload:
            return

        return self.generate_tokens(payload)


def registration_api():
    return Registration(Postgres(db), Redis(redis_conn()))
