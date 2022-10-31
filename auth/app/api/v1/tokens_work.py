from flask import Blueprint, request, jsonify
from services.tokens_service import tokens_service
from core.responses import TOKEN_WRONG_FORMAT, TOKEN_CORRECT, TOKEN_MISSING

tokens_work = Blueprint("tokens_work", __name__, url_prefix="/api/v1")


@tokens_work.route("/token", methods=["GET"])
def update_token():
    """Ендпоинт для обновления обоих токенов, принимает refresh токен,
    отдает два токена - refresh и access"""

    refresh = request.headers["Authorization"]
    tokens = tokens_service().update_tokens(refresh)
    if tokens:
        return tokens
    return jsonify(TOKEN_WRONG_FORMAT), 401


@tokens_work.route("/check", methods=["GET"])
def check():
    """Ендпоинт для проверки состояния токена клиента,
    принимает access токен, возвращает информацию о состоянии токена"""
    token = request.headers.get("Authorization")
    if token is None:
        return jsonify(TOKEN_MISSING), 400
    token = token.split(" ")
    if len(token) > 1:
        token = token[1]
    else:
        return jsonify(TOKEN_WRONG_FORMAT), 401

    if tokens_service().check_token(token):
        return jsonify(TOKEN_CORRECT)

    return jsonify(TOKEN_WRONG_FORMAT), 401
