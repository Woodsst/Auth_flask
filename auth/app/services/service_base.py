from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from storages.db_connect import redis_conn, db
from storages.postgres.db_models import User, Role
from storages.redis.redis_api import Redis


class ServiceBase:
    """Родительский класс для сервисов"""

    def __init__(self, orm: SQLAlchemy = db, cash: Redis = Redis(redis_conn)):
        self.orm: Optional[SQLAlchemy] = orm
        self.cash: Optional[Redis] = cash

    def check_password(self, password: str, user_id: str) -> bool:
        """Проверка правильности введенного пользователем пароля"""
        db_password = self.get_user_password(user_id)
        if check_password_hash(db_password, password):
            return True
        return False

    def get_user_password(self, user_id: str) -> str:
        """Получение пароля клиента из базы данных"""
        return (
            self.orm.session.query(User.password)
            .filter(User.id == user_id)
            .first()
        )[0]

    def _get_user_data(self, user_id: str) -> dict:
        """Получение данных о клиенте"""

        user_data = (
            self.orm.session.query(User, Role.role)
            .join(Role)
            .filter(User.id == user_id)
            .first()
        )

        user_data = user_data._asdict()

        return user_data
