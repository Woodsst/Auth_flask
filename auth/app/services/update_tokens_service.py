from auth.app.jwt_api import decode_refresh_token, get_token_time_to_end
from auth.app.services.service_base import ServiceBase
from auth.app.storages.db_connect import redis_conn
from auth.app.storages.redis.redis_api import Redis


class Update(ServiceBase):
    def update_tokens(self, token: str) -> dict:
        """Функция обновления токена.
        Проводится проврка наличия токена среди отработаных токенов
        и выдача новой пары токенов"""

        if self.cash.get_invalid_refresh_token(token):
            return False
        else:
            get_token_time_to_end(token)
            self.cash.set_invalid_refresh_token(
                key=token,
                value=1,  # Ключом является токен, значение неважно
                exited=get_token_time_to_end(token),
            )
            payload = decode_refresh_token(token)
            return self.generate_tokens(payload)


def update_service():
    return Update(cash=Redis(redis_conn))
