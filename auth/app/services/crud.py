import sqlalchemy.exc

from core.jaeger_tracer import d_trace
from services.service_base import ServiceBase
from storages.postgres.db_models import Role, User
from core.defaultrole import DefaultRole


class Crud(ServiceBase):
    def add_role(self, role: str, description: str) -> bool:
        """Добавление новой роли в базу"""
        return self._create_role(role, description)

    @d_trace
    def _create_role(self, role: str, description: str):
        try:
            role = Role(role=role, description=description)
            self.orm.session.add(role)
            self.orm.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.session.rollback()
            return False
        return True

    def delete_role(self, role: str) -> bool:
        """Удаление роли из базы, если есть пользователи с этой ролью,
        они получают базовую роль user"""
        return self._delete_role(role)

    @d_trace
    def _delete_role(self, role: str):
        role_id = (
            self.orm.session.query(Role.role_id)
            .filter(Role.role == role)
            .first()
        )
        if role_id is None:
            return False
        role_id = role_id[0]
        self.orm.session.query(User).filter(User.role == role_id).update(
            {"role": DefaultRole.USER_KEY.value}, synchronize_session="fetch"
        )
        self.orm.session.query(Role).filter(Role.role == role).delete()
        self.orm.session.commit()

        return True

    def change_role(
        self, role: str, change_for_description: str, change_for_role: str
    ) -> bool:
        """Изменение роли или описания роли в базе, при отсутствии роли
        возвращает False"""
        return self._change_role(role, change_for_description, change_for_role)

    @d_trace
    def _change_role(
        self, role: str, change_for_description: str, change_for_role: str
    ) -> bool:
        if len(change_for_description) > 0:
            self.orm.session.query(Role).filter(Role.role == role).update(
                {"description": change_for_description},
                synchronize_session="fetch",
            )
        if len(change_for_role) > 0:
            result = (
                self.orm.session.query(Role)
                .filter(Role.role == role)
                .update({"role": change_for_role}, synchronize_session="fetch")
            )
            if result == 0:
                return False
        self.orm.session.commit()
        return True

    @d_trace
    def all_role(self) -> dict:
        """Возвращает список всех ролей"""

        roles = self.orm.session.query(Role).all()
        return {role.role: role.description for role in roles}

    def set_user_role(self, user_id: str, role: str) -> bool:
        """Назначить пользователю роль, если роли нет или она уже задана
        возвращает False"""
        return self._set_user_role(user_id, role)

    @d_trace
    def _set_user_role(self, user_id: str, role: str) -> bool:
        role = (
            self.orm.session.query(Role.role_id)
            .filter(Role.role == role)
            .first()[0]
        )
        try:
            result = (
                self.orm.session.query(User)
                .filter(User.id == user_id)
                .update({"role": role}, synchronize_session="fetch")
            )
            if result == 0:
                return False
            self.orm.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.session.rollback()
            return False
        return True

    @d_trace
    def get_user_role(self, user_id: str) -> list:
        """Получить роль пользователя"""

        user_role = (
            self.orm.session.query(User.login, Role.role)
            .join(Role)
            .filter(User.id == user_id)
            .all()
        )
        return user_role


def crud():
    return Crud()
