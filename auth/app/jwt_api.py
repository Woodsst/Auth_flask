import datetime

import jwt

from config.settings import default_settings


def encode_access_token(payload: dict) -> str:
    """Функция для кодирования данных в jwt,
    устанавливает время жизни токена 1 час"""

    receipt_time = datetime.datetime.utcnow()
    end_time = receipt_time + datetime.timedelta(hours=1)

    payload["receipt_time"] = str(receipt_time)
    payload["end_time"] = str(end_time)

    token = jwt.encode(
        payload=payload,
        key=default_settings.JWT_access_key,
        algorithm=default_settings.JWT_access_algorithm,
    )
    return token


def encode_refresh_token(payload: dict) -> str:
    """Функция для кодирования данных в jwt,
    устанавливает время жизни токена 14 дней"""

    receipt_time = datetime.datetime.utcnow()
    end_time = receipt_time + datetime.timedelta(days=14)

    payload["receipt_time"] = str(receipt_time)
    payload["end_time"] = str(end_time)

    token = jwt.encode(
        payload=payload,
        key=default_settings.JWT_refresh_key,
        algorithm=default_settings.JWT_refresh_algorithm,
    )
    return token


def decode_access_token(token: str):
    return jwt.decode(
        token,
        key=default_settings.JWT_access_key,
        algorithms=default_settings.JWT_access_algorithm,
    )


def decode_refresh_token(token: str):
    return jwt.decode(
        token,
        key=default_settings.JWT_refresh_key,
        algorithms=default_settings.JWT_refresh_algorithm,
    )
