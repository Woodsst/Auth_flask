import abc


class BaseCash(abc.ABC):
    """Абстрактный класс для хранилища кеша и jwt токенов"""

    def __init__(self, connect):
        self.con = connect

    @abc.abstractmethod
    def get_token(self, key: str) -> dict:
        """Получить данные по ключу"""
        pass

    @abc.abstractmethod
    def set_token(self, key: str, value: str, exited: int):
        """Внести данные"""
        pass

    @abc.abstractmethod
    def pipeline(self, **kwargs):
        pass
