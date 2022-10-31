import email_validator
from flask import Blueprint, request, jsonify
from services.service_user_profile import profile_service
from services.tokens_service import token_required
from core.responses import (
    WRONG_EMAIL,
    PASSWORD_CHANGE,
    SHORT_PASSWORD,
    PASSWORDS_EQUALS,
    PASSWORD_NOT_MATCH,
    EMAIL_CHANGE,
    BAD_REQUEST,
)

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile.route("/", methods=["GET"])
@token_required()
def user_full_information():
    """Ендпоинт для запроса данных пользователя"""
    token = request.headers.get("Authorization").split(" ")

    user_data = profile_service().get_all_user_info(token[1])
    return user_data


@profile.route("/devices", methods=["GET"])
@token_required()
def user_device_history():
    """Ендпоинт для запроса истории девайсов с которых была авторизация"""
    token = request.headers.get("Authorization").split(" ")

    user_devices_data = profile_service().get_devices_user_history(token[1])
    return user_devices_data


@profile.route("/change/email", methods=["POST"])
@token_required()
def change_user_email():
    """Ендпоинт для изменения почтового адреса пользователя"""

    user_data = profile_service().data_exist(request)
    if not user_data:
        return jsonify(BAD_REQUEST), 400

    new_email = user_data.get("new_email")
    try:
        email_validator.validate_email(new_email)
    except email_validator.EmailSyntaxError:
        return jsonify(WRONG_EMAIL), 400

    token = request.headers.get("Authorization").split(" ")
    profile_service().change_email(token[1], new_email)
    return jsonify(EMAIL_CHANGE)


@profile.route("/change/password", methods=["POST"])
@token_required()
def change_user_password():
    """Ендпоинт для изменения пароля пользователя"""

    user_data = profile_service().data_exist(request)
    if not user_data:
        return jsonify(BAD_REQUEST), 400

    password = user_data.get("password")
    new_password = user_data.get("new_password")

    if profile_service().wrong_request_data(password, 8) or (
        profile_service().wrong_request_data(new_password, 8)
    ):
        return jsonify(SHORT_PASSWORD), 400

    if new_password == password:
        return jsonify(PASSWORDS_EQUALS), 400

    token = request.headers.get("Authorization").split(" ")
    if profile_service().change_password(token[1], password, new_password):
        return jsonify(PASSWORD_CHANGE)
    return jsonify(PASSWORD_NOT_MATCH), 400
