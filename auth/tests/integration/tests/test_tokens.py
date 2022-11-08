import uuid
from http import HTTPStatus

from ..testdata.data_for_test import USERS, LOGIN, TOKEN_URL
from ..utils.http_requests import registration, login


def test_update_tokens_200(http_con, clear_databases):
    """Проверка обновления токенов по refresh токену"""

    registration(http_con, USERS[0])
    tokens = login(http_con, LOGIN)

    response = http_con.get(
        f"{TOKEN_URL}token",
        headers={
            "Authorization": f"Bearer "
            f'{tokens.get("result").get("refresh-token")}',
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, dict)
    response_data = response_data.get("result")
    assert len(response_data) == 2
    assert response_data.get("access-token") != tokens.get("access-token")
    assert response_data.get("refresh-token") != tokens.get("refresh-token")


def test_update_tokens_422(http_con, clear_databases):
    """Проверка ответа при передаче не корректного токена"""

    response = http_con.get(
        f"{TOKEN_URL}token",
        headers={
            "Authorization": "bad_token",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
