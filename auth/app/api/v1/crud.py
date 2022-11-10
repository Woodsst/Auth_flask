from http import HTTPStatus

from core.responses import (
    BAD_REQUEST,
    DEFAULT_ROLE_NOT_DELETE,
    ROLE_CHANGE,
    ROLE_CREATE,
    ROLE_DELETE,
    ROLE_EXISTS,
    ROLE_NOT_EXIST,
)
from core.schemas.crud_schemas import (
    AddRoleExist,
    AddRoleRequest,
    ChangeRoleRequest,
    DeleteRoleDefaultRole,
    DeleteRoleNotExist,
    DeleteRoleRequest,
    RoleResponse,
    UserRoleRequest,
)
from core.spec_core import RouteResponse, spec
from flask import Blueprint, request
from services.crud import DefaultRole, crud, Crud
from services.tokens_service import token_required
from spectree import Response

crud_pages = Blueprint("crud_pages", __name__, url_prefix="/api/v1/crud")


@crud_pages.route("/add_role", methods=["POST"])
@token_required(admin=True)
@spec.validate(
    json=AddRoleRequest,
    resp=Response(HTTP_200=RouteResponse, HTTP_400=AddRoleExist),
    tags=["CRUD"],
    security={"apiKey": []},
)
def add_role(service: Crud = crud()):
    """Ендпоинт добавления роли, доступ только у администратора"""

    role = request.get_json().get("role")
    description = request.get_json().get("description")

    if service.add_role(role, description):
        return RouteResponse(result=ROLE_CREATE)
    return AddRoleExist(result=ROLE_EXISTS), HTTPStatus.BAD_REQUEST


@crud_pages.route("/delete_role", methods=["DELETE"])
@token_required(admin=True)
@spec.validate(
    json=DeleteRoleRequest,
    resp=Response(
        HTTP_200=RouteResponse,
        HTTP_400=DeleteRoleNotExist,
        HTTP_409=DeleteRoleDefaultRole,
    ),
    tags=["CRUD"],
    security={"apiKey": []},
)
def delete_role(service: Crud = crud()):
    """Удаление роли, если были пользователи с удаляемой ролью, они получают
    стандартную роль User"""

    role = request.get_json().get("role")

    if role == DefaultRole.USER.value or role == DefaultRole.ADMIN.value:
        return (
            DeleteRoleDefaultRole(result=DEFAULT_ROLE_NOT_DELETE),
            HTTPStatus.CONFLICT,
        )

    if service.delete_role(role):
        return RouteResponse(result=ROLE_DELETE)

    return DeleteRoleNotExist(result=ROLE_NOT_EXIST), HTTPStatus.BAD_REQUEST


@crud_pages.route("/change_role", methods=["POST"])
@token_required(admin=True)
@spec.validate(
    json=ChangeRoleRequest,
    resp=Response(
        HTTP_200=RouteResponse,
        HTTP_409=DeleteRoleDefaultRole,
        HTTP_400=DeleteRoleNotExist,
    ),
    tags=["CRUD"],
    security={"apiKey": []},
)
def change_role(service: Crud = crud()):
    """Изменение роли или описания роли, изменить можно как только роль
    так и только описание"""

    request_data = request.get_json()

    role = request_data.get("role")
    change_for_description = request_data.get("change_description")
    change_for_role = request_data.get("change_role")

    if role == DefaultRole.USER.value or role == DefaultRole.ADMIN.value:
        return (
            DeleteRoleDefaultRole(result=DEFAULT_ROLE_NOT_DELETE),
            HTTPStatus.CONFLICT,
        )

    if (
        change_for_role == DefaultRole.USER.value
        or change_for_role == DefaultRole.ADMIN.value
    ):
        return (
            DeleteRoleDefaultRole(result=DEFAULT_ROLE_NOT_DELETE),
            HTTPStatus.CONFLICT,
        )

    if service.change_role(role, change_for_description, change_for_role):
        return RouteResponse(result=ROLE_CHANGE)

    return DeleteRoleNotExist(result=ROLE_NOT_EXIST), HTTPStatus.BAD_REQUEST


@crud_pages.route("/roles", methods=["GET"])
@token_required(admin=True)
@spec.validate(
    tags=["CRUD"],
    security={"apiKey": []},
    resp=Response(HTTP_200=RoleResponse),
)
def get_roles(service: Crud = crud()):
    """Получение всех возможных ролей и их индексов"""
    roles = service.all_role()
    return RoleResponse(roles=roles)


@crud_pages.route("/set_user_role", methods=["POST"])
@token_required(admin=True)
@spec.validate(
    json=UserRoleRequest,
    resp=Response(HTTP_200=RouteResponse, HTTP_400=RouteResponse),
    tags=["CRUD"],
    security={"apiKey": []},
)
def set_user_role(service: Crud = crud()):
    """Назначить пользователю роль, задает любую из возможных ролей"""
    request_data = request.get_json()
    user_id = request_data.get("user_id")
    role = request_data.get("role")

    if service.set_user_role(user_id, role):
        return RouteResponse(result=ROLE_CHANGE)

    return RouteResponse(result=BAD_REQUEST), HTTPStatus.BAD_REQUEST
