from flask import Blueprint, request, jsonify
from services.crud import crud, DefaultRole
from services.tokens_service import token_required
from core.responses import (
    BAD_REQUEST,
    ROLE_EXISTS,
    ROLE_CREATE,
    ROLE_DELETE,
    DEFAULT_ROLE_NOT_DELETE,
    ROLE_NOT_EXIST,
    ROLE_CHANGE,
)

crud_pages = Blueprint("crud_pages", __name__, url_prefix="/api/v1/crud")


@crud_pages.route("/add_role", methods=["POST"])
@token_required(admin=True)
def add_role():
    """Ендпоинт добавления роли, доступ только у администратора"""

    request_data = request.get_json()
    role = request_data.get("role")
    description = request_data.get("description")

    if (len(role) == 0 or role is None) or (
        len(description) == 0 or description is None
    ):
        return jsonify(BAD_REQUEST), 400

    if crud().add_role(role, description):
        return jsonify(ROLE_CREATE), 200
    return jsonify(ROLE_EXISTS), 400


@crud_pages.route("/delete_role", methods=["POST"])
@token_required(admin=True)
def delete_role():
    """Удаление роли, если были пользователи с удаляемой ролью, они получают
    стандартную роль User"""

    request_data = request.get_json()
    role = request_data.get("role")
    if role == DefaultRole.USER.value or role == DefaultRole.ADMIN.value:
        return jsonify(DEFAULT_ROLE_NOT_DELETE), 400

    if crud().delete_role(role):
        return jsonify(ROLE_DELETE), 200

    return jsonify(ROLE_NOT_EXIST), 400


@crud_pages.route("/change_role", methods=["POST"])
@token_required(admin=True)
def change_role():
    """Изменение роли или описания роли, изменить можно как только роль
    так и только описание"""

    request_data = request.get_json()
    role = request_data.get("role")
    change_for_description = request_data.get("change_description")
    change_for_role = request_data.get("change_role")

    if change_for_role is None or change_for_description is None:
        return jsonify(BAD_REQUEST), 400

    if role is None or len(role) == 0:
        return jsonify(BAD_REQUEST), 400

    if crud().change_role(role, change_for_description, change_for_role):

        return jsonify(ROLE_CHANGE)

    return jsonify(ROLE_NOT_EXIST), 400


@crud_pages.route("/roles", methods=["GET"])
@token_required(admin=True)
def roles():
    roles = crud().all_role()
    return jsonify(roles)


@crud_pages.route("/set_user_role", methods=["POST"])
@token_required(admin=True)
def set_user_role():
    if crud().set_user_role(request.get_json()):
        return jsonify({"correct": "role set"})
    return jsonify({"fail": "bad request"}), 400
