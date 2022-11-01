from functools import wraps
from typing import Union

import jwt

from core.defaultrole import DefaultRole
from core.models import spec, Logout
from jwt_api import (
    get_token_time_to_end,
    decode_refresh_token,
    decode_access_token,
    generate_tokens,
)
from services.service_base import ServiceBase
from storages.db_connect import redis_conn
from flask import request, jsonify
from core.responses import (
    TOKEN_MISSING,
    TOKEN_OUTDATED,
    ACCESS_DENIED,
    TOKEN_WRONG_FORMAT,
)


class TokensService(ServiceBase):
    """Сервис для работы с обновлением и проверкой токенов"""

    def update_tokens(self, token: str) -> Union[dict, bool]:
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
            return generate_tokens(payload)

    def check_token(self, token: str) -> bool:
        """Функция проверки состояния токена"""

        if self.cash.get_token(token):
            return False
        token_time = get_token_time_to_end(token)
        if token_time:
            if token_time > 0:
                return True
            return False
        return False


def tokens_service():
    return TokensService()


@spec.validate(
    headers=Logout,
    tags=["Login"],
)
def token_required(admin=False):
    """Декоратор для проверки access токена при запросах.
    Принимает параметр указывающий на допуск администратора"""

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
                return jsonify(TOKEN_MISSING), 401

            if redis_conn.get(token):
                return jsonify(TOKEN_OUTDATED), 403

            if admin:
                payload = decode_access_token(token)
                if int(payload.get("role")) != DefaultRole.ADMIN_KEY.value:
                    return jsonify(ACCESS_DENIED), 403

            try:
                token_time = get_token_time_to_end(token)
                if token_time:
                    if token_time <= 0:
                        return jsonify(TOKEN_OUTDATED), 401
                else:
                    return jsonify(TOKEN_WRONG_FORMAT), 401

            except jwt.exceptions.InvalidSignatureError:
                return jsonify(TOKEN_WRONG_FORMAT), 401

            except jwt.exceptions.DecodeError:
                return jsonify(TOKEN_WRONG_FORMAT), 401

            return f(*args, **kwargs)

        return decorated

    return f_wrapper
