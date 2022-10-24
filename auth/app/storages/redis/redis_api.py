from storages.base import BaseCash


class Redis(BaseCash):
    def get_invalid_refresh_token(self, key: str) -> dict:
        """Получить данные по ключу"""
        return self.con.get(key)

    def set_invalid_refresh_token(self, key: str, value: str, exited: int):
        """Внести данные"""
        self.con.set(key, value, ex=exited)
