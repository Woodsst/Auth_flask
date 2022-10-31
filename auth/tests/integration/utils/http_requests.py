import json
from http.client import HTTPConnection
from requests import Session
from ..testdata.data_for_test import (
    USER_AGENT,
    REGISTRATION_URL,
    LOGIN_URL,
    USERS,
    LOGIN,
    CRUD_URL,
    DESCRIPTION,
    NEW_ROLE,
)


def registration(http_con: Session, registration_payload: dict):
    """Регистрация пользователя"""

    s = http_con.post(REGISTRATION_URL, data=json.dumps(registration_payload))
    print(s.json())

    return s


def login(http_con: Session, login_payload: dict):
    """Вход в аккаунт"""

    response = http_con.post(
        LOGIN_URL, data=json.dumps(login_payload), headers=USER_AGENT
    )

    return response.json()


def get_access_token(http_con: HTTPConnection):
    """Регистрация и логин для получения токенов"""

    registration(http_con, USERS[0])
    tokens = login(http_con, LOGIN)

    return f"Bearer {tokens.get('access-token')}"


def add_new_role(http_con: Session, token: str):

    response = http_con.post(
        f"{CRUD_URL}add_role",
        data=json.dumps({"role": NEW_ROLE, "description": DESCRIPTION}),
        headers={"Authorization": token},
    )
    return response
