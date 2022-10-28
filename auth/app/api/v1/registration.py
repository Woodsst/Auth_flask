import json

import email_validator
from flask import Blueprint, jsonify, request
from services.service_registration import registration_api
from email_validator import validate_email
from core.responses import (
    SHORT_PASSWORD,
    WRONG_EMAIL,
    WRONG_LOGIN,
    REGISTRATION_COMPLETE,
    REGISTRATION_FAILED,
)

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    user_data = json.loads(request.data)

    if (len(user_data.get("password")) < 8) or user_data.get(
        "password"
    ) is None:
        return jsonify(SHORT_PASSWORD), 400

    user_data["device"] = request.environ.get("HTTP_USER_AGENT")

    if (len(user_data.get("login")) < 2) or user_data.get("login") is None:
        return jsonify(WRONG_LOGIN), 400

    try:
        validate_email(email=user_data["email"])
    except email_validator.EmailSyntaxError:
        return jsonify(WRONG_EMAIL), 400

    response = registration_api().registration(user_data)

    if response:
        return jsonify(REGISTRATION_COMPLETE), 201

    return jsonify(REGISTRATION_FAILED), 409
