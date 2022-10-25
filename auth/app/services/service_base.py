from typing import Optional

import jwt_api as jwt
from flask import Request
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis
from werkzeug.security import generate_password_hash, check_password_hash


class ServiceBase:
    def __init__(self, db: Postgres = None, cash: Redis = None):
        self.db: Optional[Postgres] = db
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
        db_password = self.db.get_user_password(user_id)
        hash_password_from_client = generate_password_hash(password)
        db = check_password_hash(db_password, password)
        client = check_password_hash(hash_password_from_client, password)
        if db and client:
            return True
        return False
