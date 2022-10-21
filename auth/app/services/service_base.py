from storages.postgres.postgres_api import Postgres


class ServiceBase:
    def __init__(self, db: Postgres):
        self.db = db
