import abc
from flask_sqlalchemy import SQLAlchemy


class BaseStorage(abc.ABC):
    """Абстрактный класс для хранилища данных"""

    def __init__(self, orm: SQLAlchemy):
        self.orm = orm

    @abc.abstractmethod
    def get_user_data(self, user_name: str) -> dict:
        """Получение данных о клиенте"""
        pass

    @abc.abstractmethod
    def set_user(self, user_data: dict):
        """Добавление данных клиента"""
        pass

    @abc.abstractmethod
    def put_user_social(self, user_name: str):
        """Добавление социальных сетей клиента"""
        pass

    @abc.abstractmethod
    def get_user_device_history(self, user_name) -> dict:
        """Получение данных о времени и устройствах
        на которых клиент логинился в сервис"""
        pass

    @abc.abstractmethod
    def get_user_social(self, user_name) -> dict:
        """Получение данных о социальных сетях клиента"""
        pass


class BaseCash(abc.ABC):
    """Абстрактный класс для хранилища кеша и jwt токенов"""

    def __init__(self, connect):
        self.con = connect

    @abc.abstractmethod
    def get_invalid_access_token(self, key: str) -> dict:
        """Получить данные по ключу"""
        pass

    @abc.abstractmethod
    def set_invalid_access_token(self, key: str, value: str):
        """Внести данные"""
        pass
