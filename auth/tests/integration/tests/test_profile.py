import json
import uuid
from http import HTTPStatus

import pytest

from ..testdata.data_for_test import USERS, LOGIN, PROFILE_URL
from ..testdata.responses import (
    EMAIL_CHANGE,
    PASSWORD_CHANGE,
)
from ..utils.http_requests import get_access_token


def test_profile_data_200(http_con, clear_databases):
    """Проверка получаемых данных при запросе данных профиля"""
    access_token = get_access_token(http_con)

    response = http_con.get(
        PROFILE_URL,
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert len(response_data) == 3
    assert isinstance(response_data, dict)
    assert response_data.get("login") == LOGIN.get("login")
    assert response_data.get("email") == USERS[0].get("email")
    assert response_data.get("role") == "User"


def test_profile_data_401(http_con, clear_databases):
    """Проверка доступа к профилю по невалидному токену"""

    access_token = "bad token"
    response = http_con.get(
        PROFILE_URL,
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_profile_devices_200(http_con, clear_databases):
    """Проверка получаемых данных
    при запросе устройств с которых был вход в профиль"""
    access_token = get_access_token(http_con)
    response = http_con.get(
        f"{PROFILE_URL}devices?page=1&page_size=3",
        headers={
            "Authorization": access_token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json().get("history")

    assert isinstance(response_data, list)
    first_device = response_data[0]
    assert isinstance(first_device, dict)
    assert len(first_device) == 2
    assert first_device.get("device") == "python-requests/2.28.1"


def test_profile_devices_422(http_con, clear_databases):
    """Проверка доступа к получению устройств в профиле"""
    access_token = "bad token"
    response = http_con.get(
        f"{PROFILE_URL}devices",
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_profile_change_email_200(http_con, clear_databases):
    """Проверка работы смены почты клиента"""

    access_token = get_access_token(http_con)
    new_email = "iaimnew@gmail.com"
    response = http_con.post(
        f"{PROFILE_URL}change/email",
        headers={
            "Authorization": access_token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
        data=json.dumps({"new_email": new_email}),
    )

    assert response.status_code == HTTPStatus.OK

    message = response.json().get("result")
    assert message == EMAIL_CHANGE

    response = http_con.get(
        PROFILE_URL,
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
    )

    response_data = response.json()
    assert response_data.get("email") == new_email


def test_profile_change_email_401(http_con):
    """Проверка доступа к функционалу смены почты в профиле пользователя"""

    access_token = "bad token"
    response = http_con.post(
        f"{PROFILE_URL}change/email",
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "bad_email, response_status",
    [
        ("", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("asda", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("asda@asdas", HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
def test_profile_change_email_400(
    http_con, bad_email, response_status, clear_databases
):
    """Проверка передачи не валидных адресов почты"""

    access_token = get_access_token(http_con)
    response = http_con.post(
        f"{PROFILE_URL}change/email",
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
        data=json.dumps({"new_email": bad_email}),
    )
    assert response.status_code == response_status


def test_profile_change_password_200(http_con, clear_databases):
    """Проверка функционала смены пароля пользователя"""

    access_token = get_access_token(http_con)

    response = http_con.post(
        f"{PROFILE_URL}change/password",
        headers={
            "Authorization": access_token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
        data=json.dumps(
            {
                "password": USERS[0].get("password"),
                "new_password": "iamnewpassword",
            }
        ),
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.json().get("result")
    assert response_data == PASSWORD_CHANGE


@pytest.mark.parametrize(
    "bad_password, response_status, user_password",
    [
        ("", HTTPStatus.UNPROCESSABLE_ENTITY, USERS[0].get("password")),
        ("asda", HTTPStatus.UNPROCESSABLE_ENTITY, USERS[0].get("password")),
        ("asssssda", HTTPStatus.UNPROCESSABLE_ENTITY, "wrong_password"),
    ],
)
def test_profile_change_password_422(
    http_con, user_password, bad_password, response_status, clear_databases
):
    """Проверка передачи не валидных паролей и
    неправильного пароля пользователя"""

    access_token = get_access_token(http_con)
    response = http_con.post(
        f"{PROFILE_URL}change/password",
        headers={
            "Authorization": access_token,
            "X-request-Id": str(uuid.uuid4()),
        },
        data=json.dumps(
            {"password": user_password, "new_password": bad_password}
        ),
    )
    assert response.status_code == response_status
