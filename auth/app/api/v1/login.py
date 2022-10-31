from flask import Blueprint, request, jsonify
from services.login_service import login_api
from core.responses import (
    LOGOUT,
    TOKEN_WRONG_FORMAT,
    BAD_REQUEST,
    WRONG_LOGIN,
    SHORT_PASSWORD,
)
from services.tokens_service import token_required

login_page = Blueprint("login_page", __name__, url_prefix="/api/v1")


@login_page.route("/login", methods=["POST"])
def login_user():
    """Обмен логина пароля на пару токенов access refresh"""

    request_data = login_api().data_exist(request)
    if not request_data:
        return jsonify(BAD_REQUEST), 400

    login = request_data.get("login")
    if login_api().wrong_request_data(login, 0):
        return jsonify(WRONG_LOGIN), 400

    password = request_data.get("password")
    if login_api().wrong_request_data(password, 0):
        return jsonify(SHORT_PASSWORD), 400
    user_agent = request.user_agent.string

    response = login_api().login(login, password, user_agent)
    return response


@login_page.route("/logout", methods=["GET"])
@token_required()
def logout_user():
    """Логаут пользователя, вносит действующий access токен в невалидные"""

    access_token = request.headers.get("Authorization").split(" ")
    if login_api().logout(access_token[1]):
        return jsonify(LOGOUT)

    return jsonify(TOKEN_WRONG_FORMAT), 400
