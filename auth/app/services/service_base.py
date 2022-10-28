from typing import Optional

from flask import Request
from sqlalchemy.orm import scoped_session
from werkzeug.security import check_password_hash

import jwt_api as jwt
from storages.db_connect import redis_conn, db_session
from storages.postgres.db_models import User
from storages.redis.redis_api import Redis


class ServiceBase:
    """Родительский класс для сервисов"""

    def __init__(
        self, orm: scoped_session = db_session, cash: Redis = Redis(redis_conn)
    ):
        self.orm: Optional[scoped_session] = orm
        self.cash: Optional[Redis] = cash

    @staticmethod
    def generate_tokens(payload: dict) -> dict:
        """Генерация токенов"""

        access = jwt.encode_access_token(payload)
        refresh = jwt.encode_refresh_token(payload)

        return {"access-token": access, "refresh-token": refresh}

    @staticmethod
    def get_user_id_from_token(request: Request) -> str:
        """Получение id пользователя из токена"""

        token = request.headers.get("Authorization").split(" ")[1]
        return jwt.decode_access_token(token).get("id")

    def check_password(self, password: str, user_id: str) -> bool:
        """Проверка правильности введенного пользователем пароля"""
        db_password = self.get_user_password(user_id)
        if check_password_hash(db_password, password):
            return True
        return False

    def get_user_password(self, user_id: str):
        """Получение пароля клиента из базы данных"""
        return (
            self.orm.query(User.password).filter(User.id == user_id).first()
        )[0]

    @staticmethod
    def wrong_request_data(data: Optional[str], lenght: int):
        """Проверка существования и соответствия данных"""
        if data is None or len(data) <= lenght:
            return True
        return False
