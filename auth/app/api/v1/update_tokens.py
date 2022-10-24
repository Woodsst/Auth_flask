from flask import Blueprint, request, jsonify
from services.update_tokens_service import update_service

update = Blueprint("update", __name__, url_prefix="/api/v1")


@update.route("/token", methods=["GET"])
def update_token():
    refresh = request.headers["Authorize"]
    tokens = update_service().update_tokens(refresh)
    if tokens:
        return tokens
    return jsonify("error: incorrect token"), 401
