import json

from email_validator import validate_email
from auth.app.exceptions import PasswordException
from flask import Request
from auth.app.services.service_base import ServiceBase
from auth.app.storages.db_connect import db_session, redis_conn
from auth.app.storages.postgres.postgres_api import Postgres
from auth.app.storages.redis.redis_api import Redis
from werkzeug.security import generate_password_hash


class Registration(ServiceBase):
    def registration(self, request: Request) -> dict:
        """Регистрация нового пользователя"""

        user_data = json.loads(request.data)
        if self.validation_request(user_data):
            user_data["device"] = request.environ.get("HTTP_USER_AGENT")
            user_data["password"] = generate_password_hash(
                user_data["password"]
            )
            add_user = self.db.set_user(user_data)
            if add_user:
                return True
            return False

    @staticmethod
    def validation_request(user_data: dict):
        if len(user_data["password"]) < 8:
            raise PasswordException("password too short")
        validate_email(email=user_data["email"])
        return True


def registration_api():
    return Registration(Postgres(db_session), Redis(redis_conn))
