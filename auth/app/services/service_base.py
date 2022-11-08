import uuid
from typing import Optional

import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from core.defaultrole import DefaultRole
from core.jaeger_tracer import d_trace
from storages.db_connect import redis_conn, db
from storages.postgres.db_models import User, Social, UserSocial, Role
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

    @d_trace
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

    def _set_user(self, user_data: dict):
        """Добавление данных нового пользователя"""
        try:
            user_id = uuid.uuid4()
            user = User(
                login=user_data.get("login"),
                password=user_data.get("password"),
                email=user_data.get("email"),
                id=user_id,
                role=DefaultRole.USER_KEY.value,
            )
            self.orm.session.add(user)
            self.orm.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.session.rollback()
            return False
        return True

    def _set_social(self, login: str, social_name: str, social_url: str):
        user_id = User.query.filter_by(login=login).first()
        id = uuid.uuid4()
        social = Social(id=id, name=social_name)
        user_social = UserSocial(
            social_id=id, user_id=user_id.id, url=social_url
        )
        self.orm.session.add(social)
        self.orm.session.add(user_social)
        self.orm.session.commit()
