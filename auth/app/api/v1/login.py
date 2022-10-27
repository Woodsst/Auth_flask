from flask import Blueprint, request, jsonify
from services.login_service import login_api

login_page = Blueprint("login_page", __name__, url_prefix="/api/v1")


@login_page.route("/login", methods=["POST"])
def login_user():
    response = login_api().login(request)
    return response


@login_page.route("/logout", methods=["GET"])
def logout_user():
    access_token = request.headers.get("Authorization")
    if access_token is None:
        return jsonify({"message": "token is missing"})

    access_token = access_token.split(" ")
    if len(access_token) != 2:
        return jsonify({"message": "wrong token format"})

    login_api().logout(access_token[1])

    return jsonify({"message": "logout"})
