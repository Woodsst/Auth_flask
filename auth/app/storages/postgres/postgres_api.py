import uuid

import sqlalchemy
from storages.base import BaseStorage
from storages.postgres.db_models import (
    Device,
    Social,
    User,
    UserDevice,
    UserSocial,
    Role,
)


class Postgres(BaseStorage):
    def get_user_data(self, user_id: str) -> dict:
        """Получение данных о клиенте"""

        user_data = User.query.filter_by(id=user_id).first().to_dict()
        user_data["socials"] = self.get_user_social(user_id)
        user_data["devices"] = self.get_user_device_history(user_id)

        return user_data

    def set_user(self, user_data: dict):
        """Добавление данных нового клиента"""
        try:
            user_id = uuid.uuid4()
            user = User(
                login=user_data.get("login"),
                password=user_data.get("password"),
                email=user_data.get("email"),
                id=user_id,
                role=1,
            )
            self._set_device(user_data.get("device"), user_id)
            self.orm.add(user)
            self.orm.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        return True

    def _set_device(self, device: str, user_id: str):
        """Добавление нового устройства с которого клиент зашел в аккаунт"""

        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.add(device)
        self.orm.add(user_device)

    def _set_social(self, social_id: str, user_id: str, url):
        """Добавление новой социальной сети клиента"""

        user_social = UserSocial(user_id=user_id, url=url, social_id=social_id)

        self.orm.add(user_social)

    def _add_social(self, social: str) -> str:
        """Добавление социальной сети в список сетей,
        возвращает id сети для возможности добавления в список сетей клиента"""

        id = Social.query.filter_by(name=social).first()
        if id:
            return id.id
        id = uuid.uuid4()
        social_model = Social(id=id, name=social)
        self.orm.add(social_model)

        return id

    def put_user_social(self, social: str, user_id: str, url: str):
        """Добавление новой социальной сетей клиента"""

        social_id = self._add_social(social)
        self._set_social(social_id, user_id, url)
        self.orm.commit()

    def get_user_device_history(self, user_id: str) -> list:
        """Получение данных о времени и устройствах
        на которых клиент логинился в сервис"""

        device_history = (
            self.orm.query(Device.device, UserDevice.entry_time)
            .join(User)
            .join(Device)
            .filter(UserDevice.user_id == user_id)
            .all()
        )
        return device_history

    def get_user_social(self, user_id: str) -> list:
        """Получение данных о социальных сетях клиента"""

        user_social = (
            self.orm.query(Social.name, UserSocial.url)
            .join(User)
            .join(Social)
            .filter(UserSocial.user_id == user_id)
            .all()
        )
        return user_social

    def change_user_email(self, user_id: str, email: str):
        """Изменение почты клиента"""

        self.orm.query(User).filter(User.id == user_id).update(
            {"email": email}, synchronize_session="fetch"
        )
        self.orm.commit()

    def get_user_password(self, user_id: str):
        return (
            self.orm.query(User.password).filter(User.id == user_id).first()
        )[0]

    def change_user_password(self, user_id, password: str):
        """Изменение пароля клиента"""

        self.orm.query(User).filter(User.id == user_id).update(
            {"password": password}, synchronize_session="fetch"
        )
        self.orm.commit()

    def create_role(self, role: str, description: str):
        """Добавление новой роли"""
        try:
            role = Role(role=role, description=description)
            self.orm.add(role)
            self.orm.commit()
        except sqlalchemy.exc.IntegrityError:
            return False

    def delete_role(self, role: str):
        """Удаление роли, если есть пользователи с этой ролью,
        они получают базовую роль user"""

        self.orm.query(Role).filter(Role.role == role).delete()
        role_id = (
            self.orm.query(Role.role_id).filter(Role.role == role).first()
        )
        self.orm.query(User).filter(User.role == role_id).update(
            {"role": 2}, synchronize_session="fetch"
        )
        self.orm.commit()

    def change_role(
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

    def get_roles(self):
        """Возвращает все роли"""
        return self.orm.query(Role).all()

    def set_user_role(self, user_id: str, role: str):
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
            return False
        return True

    def get_user_role(self, user_id: str):
        user_role = (
            self.orm.query(User.login, Role.role)
            .join(Role)
            .filter(User.id == user_id)
            .all()
        )
        return user_role
