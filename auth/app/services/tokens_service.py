from functools import wraps
from typing import Union

import jwt
from flask import request
from spectree import Response

from core.defaultrole import DefaultRole
from core.models import spec, RouteResponse, Token
from core.responses import (
    TOKEN_OUTDATED,
    ACCESS_DENIED,
    TOKEN_WRONG_FORMAT,
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


def token_required(admin=False):
    """Декоратор для проверки access токена при запросах.
    Принимает параметр указывающий на допуск администратора"""

    def f_wrapper(f):
        @wraps(f)
        @spec.validate(
            headers=Token,
            resp=Response(HTTP_403=RouteResponse, HTTP_401=RouteResponse),
        )
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization").split(" ")
            token = token[1]
            if redis_conn.get(token):
                return RouteResponse(result=TOKEN_OUTDATED), 403

            if admin:
                payload = decode_access_token(token)
                if int(payload.get("role")) != DefaultRole.ADMIN_KEY.value:
                    return RouteResponse(result=ACCESS_DENIED), 403

            try:
                token_time = get_token_time_to_end(token)
                if token_time:
                    if token_time <= 0:
                        return RouteResponse(result=TOKEN_OUTDATED), 401
                else:
                    return RouteResponse(result=TOKEN_WRONG_FORMAT), 401

            except jwt.exceptions.InvalidSignatureError:
                return RouteResponse(result=TOKEN_WRONG_FORMAT), 401

            except jwt.exceptions.DecodeError:
                return RouteResponse(result=TOKEN_WRONG_FORMAT), 401

            return f(*args, **kwargs)

        return decorated

    return f_wrapper
