import enum
from functools import lru_cache

import sqlalchemy

from services.service_base import ServiceBase
from storages.db_connect import db_session
from storages.postgres.db_models import Role, User


class DefaultRole(enum.Enum):
    ADMIN = "admin"
    ADMIN_KEY = 1
    USER = "user"
    USER_KEY = 2


class Crud(ServiceBase):
    def add_role(self, role: str, description: str) -> bool:
        """Создание новой роли"""
        return self.__create_role(role, description)

    def __create_role(self, role: str, description: str):
        """Добавление новой роли в базу"""
        try:
            role = Role(role=role, description=description)
            self.orm.add(role)
            self.orm.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.rollback()
            return False
        return True

    def delete_role(self, request_data: dict) -> bool:
        """Удаление роли"""

        role = request_data.get("role")
        if role == DefaultRole.USER.value or role == DefaultRole.ADMIN.value:
            return False

        if self.__delete_role(role):
            return True
        return False

    def __delete_role(self, role: str):
        """Удаление роли из базы, если есть пользователи с этой ролью,
        они получают базовую роль user"""

        role_id = (
            self.orm.query(Role.role_id).filter(Role.role == role).first()
        )
        role_id = role_id[0]
        self.orm.query(User).filter(User.role == role_id).update(
            {"role": DefaultRole.USER_KEY.value}, synchronize_session="fetch"
        )
        self.orm.query(Role).filter(Role.role == role).delete()
        self.orm.commit()
        return True

    def change_role(self, request_data):
        """Изменение роли или описания роли"""

        role = request_data.get("role")
        change_for_description = request_data.get("change_description")
        change_for_role = request_data.get("change_role")

        if change_for_role is None or change_for_description is None:
            return False

        if self.__change_role(role, change_for_description, change_for_role):
            return True

        return False

    def __change_role(
        self, role: str, change_for_description: str, change_for_role: str
    ):
        """Изменение роли или описания"""
        if len(change_for_description) > 0:
            self.orm.query(Role).filter(Role.role == role).update(
                {"description": change_for_description},
                synchronize_session="fetch",
            )
        if len(change_for_role) > 0:
            result = (
                self.orm.query(Role)
                .filter(Role.role == role)
                .update({"role": change_for_role}, synchronize_session="fetch")
            )
            if result == 0:
                return False
        self.orm.commit()
        return True

    def all_role(self) -> dict:
        """Возвращает список всех ролей"""
        roles = self.orm.query(Role).all()
        return {role.role: role.description for role in roles}

    def set_user_role(self, request_data: dict):
        """Назначить пользователю роль"""

        user_id = request_data.get("user_id")
        role = request_data.get("role")
        if user_id is None or role is None:
            return False
        if self.__set_user_role(user_id, role):
            return True
        return False

    def __set_user_role(self, user_id: str, role: str):
        """Назначить пользователю роль"""
        try:
            result = (
                self.orm.query(User)
                .filter(User.id == user_id)
                .update({"role": role}, synchronize_session="fetch")
            )
            if result == 0:
                return False
            self.orm.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.rollback()
            return False
        return True

    def set_default_user_role(self, user_id: str):
        """Задать стандартную роль пользователю"""

        if self.__set_user_role(user_id, 1):
            return True
        return False

    def get_user_role(self, user_id: str) -> list:
        """Получить роль пользователя"""

        user_role = (
            self.orm.query(User.login, Role.role)
            .join(Role)
            .filter(User.id == user_id)
            .all()
        )
        return user_role


@lru_cache()
def crud():
    return Crud(db_session)
