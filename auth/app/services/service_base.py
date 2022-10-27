from typing import Optional

from flask import Request
from sqlalchemy.orm import scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

import jwt_api as jwt
from storages.db_connect import redis_conn
from storages.postgres.db_models import User
from storages.redis.redis_api import Redis


class ServiceBase:
    """Родительский класс для сервисов"""

    def __init__(self, orm: scoped_session = None, cash:
    Redis = Redis(redis_conn)):
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
        token = request.headers.get("Authorization").split(" ")[1]
        return jwt.decode_access_token(token).get("id")

    def check_password(self, password: str, user_id: str) -> bool:
        db_password = self.get_user_password(user_id)
        hash_password_from_client = generate_password_hash(password)
        db = check_password_hash(db_password, password)
        client = check_password_hash(hash_password_from_client, password)
        if db and client:
            return True
        return False

    def get_user_password(self, user_id: str):
        return (
            self.orm.query(User.password).filter(User.id == user_id).first()
        )[0]
