import jwt
from flask import Blueprint, request, jsonify
from services.tokens_service import tokens_service

tokens_work = Blueprint("tokens_work", __name__, url_prefix="/api/v1")


@tokens_work.route("/token", methods=["GET"])
def update_token():
    """Ендпоинт для обновления обоих токенов, принимает refresh токен,
    отдает два токена - refresh и access"""

    refresh = request.headers["Authorization"]
    tokens = tokens_service().update_tokens(refresh)
    if tokens:
        return tokens
    return jsonify("error: incorrect token"), 401


@tokens_work.route("/check", methods=["GET"])
def check():
    """Ендпоинт для проверки состояния токена клиента,
    принимает access токен, возвращает информацию о состоянии токена"""

    try:
        if tokens_service().check_token(request):
            return jsonify({"correct": "correct token"})
        return jsonify({"error": "token time expired"}), 401
    except jwt.exceptions.InvalidSignatureError:
        return jsonify({"error": "token is invalid"}), 401
