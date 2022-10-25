import json

from flask import Request
from services.service_base import ServiceBase
from storages.db_connect import db
from storages.db_connect import redis_conn
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis
from werkzeug.security import generate_password_hash
from exceptions import PasswordException
from email_validator import validate_email


class Registration(ServiceBase):
    """Сервис регистрации клиентов"""

    def registration(self, request: Request) -> dict:
        """Регистрация нового пользователя"""

        user_data = json.loads(request.data)
        if self.validation_request(user_data):
            user_data["device"] = request.environ.get("HTTP_USER_AGENT")
            user_data["user"]["password"] = generate_password_hash(
                user_data["user"]["password"]
            )
            add_user = self.db.set_user(user_data)
            if add_user:
                return True
            return False

    @staticmethod
    def validation_request(user_data: dict):
        """Валидация данных из тела запроса"""

        if len(user_data["user"]["password"]) < 8:
            raise PasswordException("password too short")
        validate_email(email=user_data["user"]["email"])
        return True


def registration_api():
    return Registration(Postgres(db), Redis(redis_conn))
