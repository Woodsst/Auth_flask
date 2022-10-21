import uuid
from storages.base import BaseStorage
from storages.postgres.db_models import (
    User,
    UserDevice,
    Device,
    Social,
    UserSocial,
)


class Postgres(BaseStorage):
    def get_client_data(self, user_name: str) -> dict:
        """Получение данных о клиенте"""
        return User.query.filter_by(login=user_name).first().to_dict()

    def set_client(self, user_data: dict):
        """Добавление данных клиента"""
        user_id = uuid.uuid4()
        user = User(**user_data.get("user"), id=user_id)
        self._set_device(user_data.get("device"), user_id)
        self.orm.session.add(user)
        self.orm.session.commit()

    def _set_device(self, device: str, user_id: str):
        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.session.add(device)
        self.orm.session.add(user_device)

    def _set_social(self, social_id: str, user_id: str, url):
        user_social = UserSocial(user_id=user_id, url=url, social_id=social_id)

        self.orm.session.add(user_social)

    def _add_social(self, social: str):
        id = Social.query.filter_by(name=social).first()
        if id:
            return id.id
        id = uuid.uuid4()
        social_model = Social(id=id, name=social)
        self.orm.session.add(social_model)

        return id

    def put_client_social(self, social: str, user_id: str, url: str):
        """Добавление социальных сетей клиента"""
        social_id = self._add_social(social)
        self._set_social(social_id, user_id, url)
        self.orm.session.commit()

    def get_client_device_history(self, user_id: str) -> list:
        """Получение данных о времени и устройствах
        на которых клиент логинился в сервис"""

        device_history = self.orm.session.query(
            Device.device, UserDevice.entry_time
        ).join(
            User
        ).join(
            Device
        ).filter(
            UserDevice.user_id == User.id == user_id
        ).all()
        return device_history

    def get_client_social(self, user_name) -> dict:
        """Получение данных о социальных сетях клиента"""
        pass
