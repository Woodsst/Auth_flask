from functools import wraps, lru_cache

import jwt

from jwt_api import (
    get_token_time_to_end,
    decode_refresh_token,
    decode_access_token,
)
from services.service_base import ServiceBase
from storages.db_connect import redis_conn
from storages.redis.redis_api import Redis
from flask import request, jsonify


class TokensService(ServiceBase):
    """Сервис для работы с обновлением и проверкой токенов"""

    def update_tokens(self, token: str) -> dict:
        """Функция обновления токена.
        Проводится проврка наличия токена среди отработаных токенов
        и выдача новой пары токенов, refresh токен с действующим временем
        вносится в редис в виде ключа,
        значение ключа в данном случае роли не играет"""

        if self.cash.get_token(token):
            return False
        else:
            time_to_end_token = get_token_time_to_end(token)
            if not time_to_end_token:
                return False
            self.cash.set_token(
                key=token,
                value=1,
                exited=time_to_end_token,
            )
            payload = decode_refresh_token(token)
            return self.generate_tokens(payload)

    def check_token(self, token: str):
        """Функция проверки состояния токена"""

        if self.cash.get_token(token):
            return False

        token_time = get_token_time_to_end(token)
        if token_time:
            if token_time > 0:
                return True
            return False
        return False


@lru_cache()
def tokens_service():
    return TokensService(cash=Redis(redis_conn))


def token_required(admin=False):
    def f_wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if request.headers.get("Authorization"):
                token = request.headers["Authorization"]
                token = token.split(" ")
                if len(token) > 1:
                    token = token[1]
            if not token:
                return jsonify({"message": "Token is missing !!"}), 401
            if redis_conn.get(token):
                return jsonify({"message": "Forbidden"}), 403
            if admin:
                payload = decode_access_token(token)
                if int(payload.get("role")) != 1:
                    return jsonify({"message": "Forbidden"}), 403
            try:
                token_time = get_token_time_to_end(token)
                if token_time <= 0:
                    return jsonify({"message": "Token time expired"}), 401
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({"error": "token is invalid"}), 401
            except jwt.exceptions.DecodeError:
                return jsonify({"error": "token is invalid"}), 401
            return f(*args, **kwargs)

        return decorated

    return f_wrapper
