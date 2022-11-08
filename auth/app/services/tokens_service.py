from functools import wraps
from http import HTTPStatus
from typing import Union

import pydantic
from flask import request, jsonify

from core.defaultrole import DefaultRole
from core.responses import (
    TOKEN_OUTDATED,
    ACCESS_DENIED,
    TOKEN_WRONG_FORMAT,
)
from core.schemas.token_schemas import (
    TokenRequest,
)
from jwt_api import (
    get_token_time_to_end,
    decode_refresh_token,
    decode_access_token,
    generate_tokens,
)
from services.service_base import ServiceBase
from storages.db_connect import redis_conn


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
            if not time_to_end_token or time_to_end_token <= 0:
                return False
            self.cash.set_token(
                key=token,
                value=1,
                exited=time_to_end_token,
            )
            payload = decode_refresh_token(token)
            return generate_tokens(payload)


def tokens_service():
    return TokensService()


def token_required(admin=False):
    """Декоратор для проверки access токена при запросах.
    Принимает параметр указывающий на допуск администратора"""

    def f_wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            try:
                TokenRequest(Authorization=token)
            except pydantic.error_wrappers.ValidationError:
                return (
                    jsonify(TOKEN_WRONG_FORMAT),
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                )
            token = request.headers["Authorization"]
            token = token.split(" ")
            token = token[1]
            if redis_conn.get(token):
                return jsonify(TOKEN_OUTDATED), HTTPStatus.UNAUTHORIZED

            if admin:
                payload = decode_access_token(token)
                if payload.get("role") != DefaultRole.ADMIN.value:
                    return jsonify(ACCESS_DENIED), HTTPStatus.FORBIDDEN

            token_time = get_token_time_to_end(token)
            if token_time and token_time <= 0:
                return jsonify(TOKEN_OUTDATED), HTTPStatus.UNAUTHORIZED

            return f(*args, **kwargs)

        return decorated

    return f_wrapper
