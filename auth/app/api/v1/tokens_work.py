from flask import Blueprint, request
from spectree import Response

from core.spec_core import spec, RouteResponse
from core.schemas.token_schemas import TokenOutDate, TokenRequest
from services.tokens_service import tokens_service
from core.responses import TOKEN_CORRECT, TOKEN_OUTDATED

tokens_work = Blueprint("tokens_work", __name__, url_prefix="/api/v1")


@tokens_work.route("/token", methods=["GET"])
@spec.validate(
    headers=TokenRequest,
    resp=Response(HTTP_200=RouteResponse, HTTP_401=TokenOutDate),
    tags=["Token"],
)
def update_token():
    """Ендпоинт для обновления обоих токенов, принимает refresh токен,
    отдает два токена - refresh и access"""

    refresh = request.headers["Authorization"].split(" ")
    refresh = refresh[1]
    tokens = tokens_service().update_tokens(refresh)
    if tokens:
        return RouteResponse(result=tokens)

    return TokenOutDate(result=TOKEN_OUTDATED), 401


@tokens_work.route("/check", methods=["GET"])
@spec.validate(
    headers=TokenRequest,
    resp=Response(HTTP_200=RouteResponse, HTTP_401=TokenOutDate),
    tags=["Token"],
)
def check():
    """Ендпоинт для проверки состояния токена клиента,
    принимает access токен, возвращает информацию о состоянии токена"""

    token = request.headers["Authorization"].split(" ")
    token = token[1]

    if tokens_service().check_token(token):
        return RouteResponse(result=TOKEN_CORRECT)

    return TokenOutDate(result=TOKEN_OUTDATED), 401
