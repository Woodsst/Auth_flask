from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis


class ServiceBase:
    def __init__(self, db: Postgres, cash: Redis):
        self.db = db
        self.cash = cash
