import jwt
from flask import Blueprint, request, jsonify
from services.tokens_service import tokens_service, token_required

tokens_work = Blueprint("update", __name__, url_prefix="/api/v1")


@tokens_work.route("/token", methods=["GET"])
@token_required
def update_token():
    refresh = request.headers["Authorization"]
    tokens = tokens_service().update_tokens(refresh)
    if tokens:
        return tokens
    return jsonify("error: incorrect token"), 401


@tokens_work.route("/check", methods=["GET"])
def check():
    try:
        if tokens_service().check_token(request):
            return jsonify({"correct": "correct token"})
        else:
            return jsonify({"error": "token time expired"}), 401
    except jwt.exceptions.InvalidSignatureError:
        return jsonify({"error": "token is invalid"}), 401
