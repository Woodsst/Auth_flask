import enum

from services.service_base import ServiceBase
from storages.db_connect import db_session
from storages.postgres.postgres_api import Postgres


class DefaultRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class Crud(ServiceBase):
    def create_role(self, request_data: dict) -> bool:
        """Создание новой роли"""

        role = request_data.get("role")
        description = request_data.get("description")
        if (len(role) == 0 or role is None) or (
            len(description) == 0 or description is None
        ):
            return False
        if self.db.create_role(role, description):
            return True
        return False

    def delete_role(self, request_data: dict) -> bool:
        """Удаление роли, все владельцы роли
        будут понижены до базовой роли user"""

        role = request_data.get("role")
        if role == DefaultRole.USER.value or role == DefaultRole.ADMIN.value:
            return False

        if self.db.delete_role(role):
            return True
        return False

    def change_role(self, request_data):
        """Изменение роли или описания роли"""
        role = request_data.get("role")
        change_for_description = request_data.get("change_description")
        change_for_role = request_data.get("change_role")
        if change_for_role is None or change_for_description is None:
            return False
        if self.db.change_role(role, change_for_description, change_for_role):
            return True
        return False

    def all_role(self) -> dict:
        """Возвращает список всех ролей"""
        roles = self.db.get_roles()
        return {role.role: role.description for role in roles}

    def set_user_role(self, request_data: dict):
        """Назначить пользователю роль"""
        user_id = request_data.get("user_id")
        role = request_data.get("role")
        if user_id is None or role is None:
            return False
        if self.db.set_user_role(user_id, role):
            return True
        return False

    def set_default_user_role(self, user_id: str):
        """Задать стандартную роль пользователю"""

        if self.db.set_user_role(user_id, 1):
            return True
        return False

    def get_user_role(self, user_id: str) -> list:
        """Получить роль пользователя"""
        return self.db.get_user_role(user_id)


def crud():
    return Crud(Postgres(db_session))
