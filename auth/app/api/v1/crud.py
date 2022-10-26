from flask import Blueprint, request, jsonify
from services.crud import crud

crud_pages = Blueprint("crud_pages", __name__, url_prefix="/api/v1/crud")


@crud_pages.route("/add_role", methods=["POST"])
def add_role():
    if crud().add_role(request.get_json()):
        return jsonify({"correct": "role created"})
    return jsonify({"fail": "bad request"}), 400


@crud_pages.route("/delete_role", methods=["POST"])
def delete_role():
    if crud().delete_role(request.get_json()):
        return jsonify({"correct": "role delete"})
    return jsonify({"fail": "bad request"}), 400


@crud_pages.route("/change_role", methods=["POST"])
def change_role():
    if crud().change_role(request.get_json()):
        return jsonify({"correct": "role change"})
    return jsonify({"fail": "bad request"}), 400


@crud_pages.route("/roles", methods=["GET"])
def roles():
    roles = crud().all_role()
    return jsonify(roles)


@crud_pages.route("/set_user_role", methods=["POST"])
def set_user_role():
    if crud().set_user_role(request.get_json()):
        return jsonify({"correct": "role set"})
    return jsonify({"fail": "bad request"}), 400
