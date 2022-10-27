import json
from functools import lru_cache

from services.service_base import ServiceBase
from storages.db_connect import db_session
from storages.postgres.db_models import (
    User,
    Device,
    UserDevice,
    Role,
)
from flask import Request
from email_validator import validate_email
from werkzeug.security import generate_password_hash

from exceptions import PasswordException


class ProfileService(ServiceBase):
    def get_all_user_info(self, request: Request):
        """Получение данных пользователя"""

        user_id = self.get_user_id_from_token(request)

        user_data = self.get_user_data(user_id)
        return self._format_user_data(user_data)

    @staticmethod
    def _format_user_data(user_data: dict) -> dict:
        """Форматирование данных из базы для отправки пользователю"""

        role = user_data.get("role")
        user_data = user_data.get("User").to_dict()
        return json.dumps(
            {
                "login": user_data.get("login"),
                "email": user_data.get("email"),
                "role": role,
            }
        )

    def get_devices_user_history(self, request: Request):
        """Получение устройств с которых входили в профиль"""

        user_id = self.get_user_id_from_token(request)
        raw_history = self.get_user_device_history(user_id)
        history = self._format_devices_history(raw_history)
        return history

    @staticmethod
    def _format_devices_history(raw_history: list) -> dict:
        """Форматирование данных истории устройств для отправки пользователю"""

        history = []
        for entry in raw_history:
            entry = entry._asdict()
            entry_time = entry.get("entry_time")
            entry["entry_time"] = str(entry_time)
            history.append(entry)
        return history

    def change_email(self, request: Request):
        """Изменение почты пользователя"""

        user_data = json.loads(request.data)
        new_email = user_data.get("new_email")
        validate_email(new_email)
        user_id = self.get_user_id_from_token(request)
        self.change_user_email(user_id, new_email)

    def change_password(self, request: Request):
        """Изменение пароля пользователя"""

        user_id = self.get_user_id_from_token(request)
        user_data = json.loads(request.data)
        password = user_data.get("password")
        new_password = user_data.get("new_password")

        if len(new_password) < 8:
            raise PasswordException("password too short")

        if self.check_password(password, user_id):
            if new_password == password:
                return False
            new_password = generate_password_hash(new_password)
            self.change_user_password(user_id, new_password)
            return True
        return False

    def change_user_email(self, user_id: str, email: str):
        """Запрос в базу для изменения почты клиента"""

        self.orm.query(User).filter(User.id == user_id).update(
            {"email": email}, synchronize_session="fetch"
        )
        self.orm.commit()

    def change_user_password(self, user_id, password: str):
        """Запрос в базу для изменения пароля клиента"""

        self.orm.query(User).filter(User.id == user_id).update(
            {"password": password}, synchronize_session="fetch"
        )
        self.orm.commit()

    def get_user_data(self, user_id: str) -> dict:
        """Получение данных о клиенте"""

        user_data = (
            self.orm.query(User, Role.role)
            .join(Role)
            .filter(User.id == user_id)
            .first()
        )

        user_data = user_data._asdict()

        return user_data

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


@lru_cache()
def profile_service():
    return ProfileService(db_session)
