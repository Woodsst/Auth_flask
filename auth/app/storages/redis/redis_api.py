from storages.base import BaseCash


class Redis(BaseCash):

    def get_invalid_access_token(self, key: str) -> dict:
        """Получить данные по ключу"""
        return self.con.get(key)

    def set_invalid_access_token(self, key: str, value: str):
        """Внести данные"""
        self.con.set(key, value)
