import json
from http.client import HTTPConnection
from ..testdata.data_for_test import (
    USER_AGENT,
    REGISTRATION_URL,
    LOGIN_URL,
    USERS,
    LOGIN,
)


def registration(http_con: HTTPConnection, registration_payload: dict):
    """Регистрация пользователя"""

    http_con.request(
        "POST",
        REGISTRATION_URL,
        body=json.dumps(registration_payload),
        headers=USER_AGENT,
    )
    response = http_con.getresponse()

    return response


def login(http_con: HTTPConnection, login_payload: dict):
    """Вход в аккаунт"""

    http_con.request("POST", LOGIN_URL, body=json.dumps(login_payload))

    return json.loads(http_con.getresponse().read())


def get_access_token(http_con: HTTPConnection):
    """Регистрация и логин для получения токенов"""

    registration(http_con, USERS[0])
    tokens = login(http_con, LOGIN)

    return f"Bearer {tokens.get('access-token')}"