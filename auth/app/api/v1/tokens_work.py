from http import HTTPStatus

from core.responses import TOKEN_OUTDATED
from core.schemas.token_schemas import TokenOutDate, TokenRequest
from core.spec_core import RouteResponse, spec
from flask import Blueprint, request
from services.tokens_service import tokens_service, TokensService
from spectree import Response

tokens_work = Blueprint("tokens_work", __name__, url_prefix="/api/v1")


@tokens_work.route("/token", methods=["GET"])
@spec.validate(
    headers=TokenRequest,
    resp=Response(HTTP_200=RouteResponse, HTTP_401=TokenOutDate),
    tags=["Token"],
)
def update_token(service: TokensService = tokens_service()):
    """Ендпоинт для обновления обоих токенов, принимает refresh токен,
    отдает два токена - refresh и access"""

    refresh = request.headers["Authorization"].split(" ")
    refresh = refresh[1]
    tokens = service.update_tokens(refresh)
    if tokens:
        return RouteResponse(result=tokens)

    return TokenOutDate(result=TOKEN_OUTDATED), HTTPStatus.UNAUTHORIZED
