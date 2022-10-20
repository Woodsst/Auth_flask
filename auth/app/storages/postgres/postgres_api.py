from storages.base import BaseStorage
from storages.postgres.db_models import User


class Postgres(BaseStorage):

    def get_client_data(self, client_name: str) -> dict:
        """Получение данных о клиенте"""
        return User.query.filter_by(login=client_name).first().to_dict()

    def set_client(self, client_data: dict):
        """Добавление данных клиента"""

        client = User(**client_data)
        self.orm.session.add(client)
        self.orm.session.commit()

    def put_client_social(self, client_name: str):
        """Добавление социальных сетей клиента"""
        pass

    def get_client_device_history(self, client_name) -> dict:
        """Получение данных о времени и устройствах
        на которых клиент логинился в сервис"""
        pass

    def get_client_social(self, client_name) -> dict:
        """Получение данных о социальных сетях клиента"""
        pass
