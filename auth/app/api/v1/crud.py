from flask import Blueprint, request, jsonify
from services.crud import crud
from services.tokens_service import token_required
from core.responses import BAD_REQUEST, ROLE_EXISTS

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
        return jsonify({"correct": "role created"})
    return jsonify(ROLE_EXISTS), 400


@crud_pages.route("/delete_role", methods=["POST"])
@token_required(admin=True)
def delete_role():
    if crud().delete_role(request.get_json()):
        return jsonify({"correct": "role delete"})
    return jsonify({"fail": "bad request"}), 400


@crud_pages.route("/change_role", methods=["POST"])
@token_required(admin=True)
def change_role():
    if crud().change_role(request.get_json()):
        return jsonify({"correct": "role change"})
    return jsonify({"fail": "bad request"}), 400


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
