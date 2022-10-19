import abc
from flask_sqlalchemy import SQLAlchemy


class BaseStorage(abc.ABC):
    """Абстрактный класс для хранилища данных"""

    def __init__(self, orm: SQLAlchemy):
        self.orm = orm

    @abc.abstractmethod
    def get_client_data(self, client_name: str) -> dict:
        """Получение данных о клиенте"""
        pass

    @abc.abstractmethod
    def set_client(self, client_data: dict):
        """Добавление данных клиента"""
        pass

    @abc.abstractmethod
    def put_client_social(self, client_name: str):
        """Добавление социальных сетей клиента"""
        pass

    @abc.abstractmethod
    def get_client_device_history(self, client_name) -> dict:
        """Получение данных о времени и устройствах
        на которых клиент логинился в сервис"""
        pass

    @abc.abstractmethod
    def get_client_social(self, client_name) -> dict:
        """Получение данных о социальных сетях клиента"""
        pass


class BaseCash(abc.ABC):
    """Абстрактный класс для хранилища кеша и jwt токенов"""

    def __init__(self, connect):
        self.con = connect

    @abc.abstractmethod
    def get(self, key: str) -> dict:
        """Получить данные по ключу"""
        pass

    @abc.abstractmethod
    def set(self, key: str, value: str):
        """Внести данные"""
        pass
