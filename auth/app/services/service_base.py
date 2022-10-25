import jwt_api as jwt
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
