import uuid
from functools import lru_cache

import sqlalchemy

from services.service_base import ServiceBase
from storages.db_connect import db_session
from storages.postgres.db_models import Device, UserDevice, User
from werkzeug.security import generate_password_hash
from services.crud import DefaultRole


class Registration(ServiceBase):
    def registration(self, user_data: dict) -> dict:
        """Хеширование пароля и добавление нового пользователя"""

        user_data["password"] = generate_password_hash(user_data["password"])
        return self.set_user(user_data)

    def set_user(self, user_data: dict):
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
            self._set_device(user_data.get("device"), user_id)
            self.orm.add(user)
            self.orm.commit()
        except sqlalchemy.exc.IntegrityError:
            self.orm.rollback()
            return False
        return True

    def _set_device(self, device: str, user_id: str):
        """Добавление нового устройства с которого клиент зашел в аккаунт"""

        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.add(device)
        self.orm.add(user_device)


@lru_cache()
def registration_api():
    return Registration(db_session)
