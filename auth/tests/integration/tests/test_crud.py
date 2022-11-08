import json
import uuid
from http import HTTPStatus

import pytest
from ..utils.http_requests import (
    login,
    add_new_role,
    registration,
    get_access_token,
)
from ..testdata.data_for_test import (
    ADMIN_LOGIN,
    CRUD_URL,
    NEW_ROLE,
    DESCRIPTION,
    USERS,
    PROFILE_URL,
)
from ..testdata.responses import (
    ROLE_DELETE,
    DEFAULT_ROLE_NOT_DELETE,
    ROLE_CHANGE,
    ACCESS_DENIED,
    ROLE_NOT_EXIST,
)
from ..utils.db_requests import registration_admin, get_user_id


def test_add_role_200(http_con, clear_databases, postgres_con):
    """Проверка добавления новой роли и её описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"
    response = add_new_role(http_con, token)

    assert response.status_code == HTTPStatus.OK

    response = http_con.get(
        f"{CRUD_URL}roles",
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )
    response = response.json().get("roles")
    assert isinstance(response, dict)
    assert len(response) == 3
    assert response.get(NEW_ROLE) == DESCRIPTION


@pytest.mark.parametrize(
    "role, description, status_code",
    [
        ("", "", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("", "asd", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("a", "asd", HTTPStatus.UNPROCESSABLE_ENTITY),
        (None, None, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
def test_add_role_422(
    http_con, postgres_con, role, description, status_code, clear_databases
):
    """Проверка передачи невалидных ролей и описаний"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.post(
        f"{CRUD_URL}add_role",
        data=json.dumps({"role": role, "description": description}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == status_code


def test_delete_role_200(http_con, postgres_con, clear_databases):
    """Проверка удаления роли, при удалении роли,
    если роль была у пользователей, их роль меняется на User"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    add_new_role(http_con, token)
    registration(http_con, USERS[0])
    user_id = get_user_id(postgres_con)

    http_con.post(
        f"{CRUD_URL}set_user_role",
        data=json.dumps({"role": NEW_ROLE, "user_id": user_id}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )

    response = http_con.delete(
        f"{CRUD_URL}delete_role",
        data=json.dumps({"role": NEW_ROLE}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.OK

    message = response.json().get("result")
    assert message == ROLE_DELETE

    response = http_con.get(
        f"{CRUD_URL}roles",
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )
    response_data = response.json()
    assert response_data.get(NEW_ROLE) is None
    token = login(http_con, USERS[0])
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.get(
        PROFILE_URL,
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )
    response_data = response.json()

    assert response_data.get("role") == "User"


@pytest.mark.parametrize(
    "role, status_code, message",
    [
        ("", HTTPStatus.BAD_REQUEST, ROLE_NOT_EXIST),
        ("Admin", HTTPStatus.CONFLICT, DEFAULT_ROLE_NOT_DELETE),
        ("User", HTTPStatus.CONFLICT, DEFAULT_ROLE_NOT_DELETE),
    ],
)
def test_delete_role_400(
    postgres_con, http_con, clear_databases, role, status_code, message
):
    """Проверка невалидных запросов"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.delete(
        f"{CRUD_URL}delete_role",
        data=json.dumps({"role": role}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == status_code
    assert response.json() == message


def test_change_role_200(postgres_con, http_con, clear_databases):
    """Проверка изменения роли и описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"
    add_new_role(http_con, token)

    change_role = "change_role"
    change_desc = "change_description"

    response = http_con.post(
        f"{CRUD_URL}change_role",
        data=json.dumps(
            {
                "role": NEW_ROLE,
                "change_role": change_role,
                "change_description": change_desc,
            }
        ),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == HTTPStatus.OK

    message = response.json()
    assert message == ROLE_CHANGE

    response = http_con.get(
        f"{CRUD_URL}roles",
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )
    response_data = response.json()
    assert response_data.get("roles").get(change_role) == change_desc


@pytest.mark.parametrize(
    "role, desc, status_code",
    [
        ("Admin", "", HTTPStatus.CONFLICT),
        ("User", "", HTTPStatus.CONFLICT),
        (None, "", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("", None, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
def test_change_role_400(
    postgres_con, http_con, clear_databases, role, desc, status_code
):
    """Проверка невалидных запросов на изменение роли и описания"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"
    add_new_role(http_con, token)

    response = http_con.post(
        f"{CRUD_URL}change_role",
        data=json.dumps(
            {"role": NEW_ROLE, "change_role": role, "change_description": desc}
        ),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )

    assert response.status_code == status_code


def test_set_user_role_200(http_con, postgres_con, clear_databases):
    """Проверка изменения роли пользователя"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    add_new_role(http_con, token)
    registration(http_con, USERS[0])
    user_id = get_user_id(postgres_con)

    response = http_con.post(
        f"{CRUD_URL}set_user_role",
        data=json.dumps({"role": NEW_ROLE, "user_id": user_id}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.OK

    message = response.json()
    assert message == ROLE_CHANGE

    token = login(http_con, USERS[0])
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.get(
        PROFILE_URL,
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )
    response_data = response.json()

    assert response_data.get("role") == NEW_ROLE


@pytest.mark.parametrize(
    "user_id, role",
    [
        ("asdasd", ""),
        (None, ""),
        ("", None),
    ],
)
def test_set_user_role_400(
    http_con, postgres_con, clear_databases, role, user_id
):
    """Проверка не валидных запросов изменения роли пользователя"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.post(
        f"{CRUD_URL}set_user_role",
        data=json.dumps({"role": role, "user_id": user_id}),
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
            "X-request-Id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_roles(http_con, postgres_con, clear_databases):
    """Проверка получения списка всех ролей"""

    registration_admin(postgres_con)
    token = login(http_con, ADMIN_LOGIN)
    token = f"Bearer {token.get('result').get('access-token')}"

    response = http_con.get(
        f"{CRUD_URL}roles",
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json().get("roles")
    assert len(response_data) == 2
    assert response_data.get("Admin") == "full access"
    assert response_data.get("User") == "default access"


def test_get_add_roles_400(http_con, postgres_con, clear_databases):
    """Проверка запроса без доступа для получения списка всех ролей"""

    token = get_access_token(http_con)

    response = http_con.get(
        f"{CRUD_URL}roles",
        headers={"Authorization": token, "X-request-Id": str(uuid.uuid4())},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

    message = response.json()
    assert message == ACCESS_DENIED
