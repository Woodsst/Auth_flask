from http import HTTPStatus

from flask import redirect


from config.settings import settings
from config.limiter import limiter
from core.responses import LOGOUT, TOKEN_WRONG_FORMAT
from core.schemas.login_schemas import (LoginPasswordNotMatch, LoginRequest,
                                        LoginUserNotMatch)
from core.spec_core import RouteResponse, spec
from flask import Blueprint, request
from services.login_service import login_api
from services.tokens_service import token_required
from spectree import Response

login_page = Blueprint("login_page", __name__, url_prefix="/api/v1")


@login_page.route("/login", methods=["POST"])
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    json=LoginRequest,
    resp=Response(
        HTTP_200=RouteResponse,
        HTTP_403=LoginPasswordNotMatch,
        HTTP_401=LoginUserNotMatch,
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


@login_page.route("/login/yandex_oauth", methods=["GET"])
@spec.validate(tags=["Login"])
def yandex_oauth():
    """Перенаправление клиента на страницу yandex
    для предоставления доступа к его данным"""
    return redirect(settings.yandex_oauth_authorize)


@login_page.route("/oauth", methods=["GET"])
@spec.validate(resp=Response(HTTP_200=RouteResponse), tags=["Login"])
def oauth():
    """Аутентификация или регистрация пользователя через yandex"""

    code = request.url.split("=")
    tokens = login_api().get_tokens(code[1])
    result = login_api().oauth(
        tokens=tokens, user_agent=request.user_agent.string
    )
    return result


@login_page.route("/logout", methods=["DELETE"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    resp=Response(HTTP_200=RouteResponse, HTTP_400=RouteResponse),
    tags=["Login"],
    security={"apiKey": []},
)
def logout_user():
    """Логаут пользователя, вносит действующие токены в невалидные"""

    access_token = request.headers.get("Authorization").split(" ")
    if login_api().logout(access_token[1]):
        return RouteResponse(result=LOGOUT), HTTPStatus.OK

    return RouteResponse(result=TOKEN_WRONG_FORMAT), HTTPStatus.BAD_REQUEST
