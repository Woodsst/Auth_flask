import datetime

import jwt
from config.settings import settings


def encode_access_token(payload: dict) -> str:
    """Функция для кодирования данных в jwt,
    устанавливает время жизни токена 1 час"""

    receipt_time = datetime.datetime.utcnow()
    end_time = receipt_time + datetime.timedelta(hours=1)

    payload["receipt_time"] = str(receipt_time)
    payload["end_time"] = str(end_time)
    payload["token"] = "access"

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_access_key,
        algorithm=settings.JWT_algorithm,
    )
    return token


def encode_refresh_token(payload: dict) -> str:
    """Функция для кодирования данных в jwt,
    устанавливает время жизни токена 14 дней"""

    receipt_time = datetime.datetime.utcnow()
    end_time = receipt_time + datetime.timedelta(days=14)

    payload["receipt_time"] = str(receipt_time)
    payload["end_time"] = str(end_time)
    payload["token"] = "refresh"

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_refresh_key,
        algorithm=settings.JWT_algorithm,
    )
    return token


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        key=settings.JWT_access_key,
        algorithms=settings.JWT_algorithm,
    )


def decode_refresh_token(token: str) -> dict:
    return jwt.decode(
        token,
        key=settings.JWT_refresh_key,
        algorithms=settings.JWT_algorithm,
    )


def get_token_time_to_end(token: str) -> int:
    """Функция получения остатка времени работы токена"""
    try:
        payload = decode_refresh_token(token)
    except jwt.exceptions.InvalidSignatureError:
        payload = decode_access_token(token)
    except jwt.exceptions.DecodeError:
        return
    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
        end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )
    return int(time_for_exited)


def generate_tokens(payload: dict) -> dict:
    """Генерация токенов, access токен, содержит refresh"""

    refresh = encode_refresh_token(payload)
    payload["refresh"] = refresh
    access = encode_access_token(payload)

    return {"access-token": access, "refresh-token": refresh}


def get_user_id_from_token(token: str) -> str:
    """Получение id пользователя из токена"""
    return decode_access_token(token).get("id")


def decode_yandex_jwt(token: str):
    return jwt.decode(
        token, key=settings.yandex_client_secret, algorithms="HS256"
    )
