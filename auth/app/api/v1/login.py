from flask import Blueprint, request, jsonify
from spectree import Response

from core.models import spec, LoginRequest, RouteResponse
from core.responses import (
    LOGOUT,
    TOKEN_WRONG_FORMAT,
)
from services.login_service import login_api
from services.tokens_service import token_required

login_page = Blueprint("login_page", __name__, url_prefix="/api/v1")


@login_page.route("/login", methods=["POST"])
@spec.validate(
    json=LoginRequest,
    resp=Response(
        HTTP_200=RouteResponse, HTTP_400=RouteResponse, HTTP_401=RouteResponse
    ),
    tags=["Login"],
)
def login_user():
    """Обмен логина пароля на пару токенов access refresh"""

    user_agent = request.user_agent.string
    login = request.get_json().get("login")
    password = request.get_json().get("password")

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
