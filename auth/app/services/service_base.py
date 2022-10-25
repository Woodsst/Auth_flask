import jwt_api as jwt
from flask import Request
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis


class ServiceBase:
    def __init__(self, db: Postgres = None, cash: Redis = None):
        self.db = db
        self.cash = cash

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
