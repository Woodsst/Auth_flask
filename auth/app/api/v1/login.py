import json

from flask import Blueprint, request, jsonify
from services.login_service import login_api
from core.responses import (
    WRONG_LOGIN,
    SHORT_PASSWORD,
    TOKEN_MISSING,
    LOGOUT,
    TOKEN_WRONG_FORMAT,
)

login_page = Blueprint("login_page", __name__, url_prefix="/api/v1")


@login_page.route("/login", methods=["POST"])
def login_user():
    """Обмен логина пароля на пару токенов access refresh"""

    request_data = json.loads(request.data)
    login = request_data.get("login")
    password = request_data.get("password")

    if login_api().wrong_request_data(login, 2):
        return jsonify(WRONG_LOGIN), 400

    if login_api().wrong_request_data(password, 7):
        return jsonify(SHORT_PASSWORD), 400

    response = login_api().login(login, password)
    return response


@login_page.route("/logout", methods=["GET"])
def logout_user():
    """Логаут пользователя, вносит действующий access токен в невалидные"""

    access_token = request.headers.get("Authorization")
    if access_token is None:
        return jsonify(TOKEN_MISSING), 400

    access_token = access_token.split(" ")
    if len(access_token) != 2:
        return jsonify(TOKEN_WRONG_FORMAT), 400

    if login_api().logout(access_token[1]):
        return jsonify(LOGOUT)

    return jsonify(TOKEN_WRONG_FORMAT), 400
