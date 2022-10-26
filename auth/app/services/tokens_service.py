from functools import wraps

import jwt

from jwt_api import (
    get_token_time_to_end,
    decode_refresh_token,
)
from services.service_base import ServiceBase
from storages.db_connect import redis_conn
from storages.redis.redis_api import Redis
from flask import Request, request, jsonify


class TokensService(ServiceBase):
    """Сервис для работы с обновлением и проверкой токенов"""

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

    @staticmethod
    def check_token(request: Request):
        """Функция проверки состояния токена"""

        token = request.headers["Authorization"]
        token = token.split(" ")[1]
        token_time = get_token_time_to_end(token)
        if token_time > 0:
            return True
        return False


def tokens_service():
    return TokensService(cash=Redis(redis_conn))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401
        try:
            token_time = get_token_time_to_end(token)
            if token_time <= 0:
                return jsonify({"message": "Token time expired"}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"error": "token is invalid"}), 401
        return f(*args, **kwargs)

    return decorated
