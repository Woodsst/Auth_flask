from http import HTTPStatus

from flask import redirect
import requests

from config.settings import settings
from config.limiter import limiter
from core.providers import Providers
from core.responses import LOGOUT, TOKEN_WRONG_FORMAT
from core.schemas.login_schemas import (
    LoginPasswordNotMatch,
    LoginRequest,
    LoginUserNotMatch,
    AuthorizeProvider,
)
from core.spec_core import RouteResponse, spec
from flask import Blueprint, request
from services.login_service import login_api, LoginAPI
from services.oauth_service import VKOauth, YandexOauth
from services.tokens_service import token_required
from spectree import Response
from user_agents import parse

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
def login_user(service: LoginAPI = login_api()):
    """Обмен логина пароля на пару токенов access refresh"""

    ua_string = request.headers.get("User-Agent")
    is_pc = parse(ua_string).is_pc
    user_agent = request.user_agent.string
    login_ip = requests.get(settings.get_ip).json()["origin"]
    login = request.get_json().get("login")
    password = request.get_json().get("password")

    response = service.login(login, password, user_agent, is_pc, login_ip)
    return response


@login_page.route("/login/oauth", methods=["GET"])
@spec.validate(query=AuthorizeProvider, tags=["Login"])
def yandex_oauth():
    """Перенаправление клиента на страницу провайдера
    для предоставления доступа к данным пользователя"""
    provider = request.args.get("provider")
    providers = {
        Providers.VK.value: settings.vk.oauth_authorize,
        Providers.YANDEX.value: settings.yandex.oauth_authorize,
    }
    return redirect(providers[provider])


@login_page.route("/oauth", methods=["GET"])
@spec.validate(resp=Response(HTTP_200=RouteResponse), deprecated=True)
def oauth(
    service: LoginAPI = login_api(),
    vk: VKOauth = VKOauth(),
    yandex: YandexOauth = YandexOauth(),
):
    """Аутентификация или регистрация пользователя через провайдера"""

    ua_string = request.headers.get("User-Agent")
    is_pc = parse(ua_string).is_pc
    login_ip = requests.get(settings.get_ip).json()["origin"]
    code = request.url.split("=")

    if Providers.VK.value in request.url:
        tokens = vk.get_tokens(code[1])
        client_info = vk.get_client_info(tokens)
        provider = Providers.VK

    if Providers.YANDEX.value in request.url:
        tokens = yandex.get_tokens(code[2])
        client_info = yandex.get_client_info(tokens)
        provider = Providers.YANDEX

    return service.oauth_authentication(
        provider=provider.value,
        login=client_info.get("login"),
        password=client_info.get("password"),
        email=client_info.get("email"),
        user_agent=ua_string,
        is_pc=is_pc,
        login_ip=login_ip,
    )


@login_page.route("/logout", methods=["DELETE"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    resp=Response(HTTP_200=RouteResponse, HTTP_400=RouteResponse),
    tags=["Login"],
    security={"apiKey": []},
)
def logout_user(service: LoginAPI = login_api()):
    """Логаут пользователя, вносит действующие токены в невалидные"""

    access_token = request.headers.get("Authorization").split(" ")
    if service.logout(access_token[1]):
        return RouteResponse(result=LOGOUT), HTTPStatus.OK

    return RouteResponse(result=TOKEN_WRONG_FORMAT), HTTPStatus.BAD_REQUEST
