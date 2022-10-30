import json

from flasgger import swag_from
import email_validator
from flask import Blueprint, jsonify, request

from documentation.registrtion_page import registrtion_dict
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


@swag_from(registrtion_dict)
@registration_page.route("/registration", methods=["POST"])
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    user_data = json.loads(request.data)

    if registration_api().wrong_request_data(user_data.get("password"), 8):
        return jsonify(SHORT_PASSWORD), 400

    if registration_api().wrong_request_data(user_data.get("login"), 2):
        return jsonify(WRONG_LOGIN), 400

    try:
        validate_email(email=user_data["email"])
    except email_validator.EmailSyntaxError:
        return jsonify(WRONG_EMAIL), 400

    response = registration_api().registration(user_data)

    if response:
        return jsonify(REGISTRATION_COMPLETE), 201

    return jsonify(REGISTRATION_FAILED), 409
