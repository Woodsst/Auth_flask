import email_validator
from flask import Blueprint, request, jsonify
from auth.app.services.service_user_profile import profile_service

from auth.app.exceptions import PasswordException

profile = Blueprint("profile", __name__, url_prefix="/api/v1")


@profile.route("/profile", methods=["GET"])
def user_full_information():
    """Ендпоинт для запроса данных пользователя"""

    user_data = profile_service().get_all_user_info(request)
    return user_data


@profile.route("/profile/devices", methods=["GET"])
def user_device_history():
    """Ендпоинт для запроса истории девайсов с которых была авторизация"""

    user_devices_data = profile_service().get_devices_user_history(request)
    return user_devices_data


@profile.route("/profile/socials", methods=["GET"])
def user_socials():
    """Ендпоинт списка социальных сетей пользователя"""

    user_socials_data = profile_service().get_socials(request)
    return user_socials_data


@profile.route("/profile/change/email", methods=["POST"])
def change_user_email():
    """Ендпоинт для изменения почтового адреса пользователя"""

    try:
        profile_service().change_email(request)
        return jsonify({"correct": "email changed"})
    except email_validator.EmailSyntaxError:
        return jsonify({"error": "The email address is not valid"}), 400


@profile.route("/profile/change/password", methods=["POST"])
def change_user_password():
    """Ендпоинт для изменения пароля пользователя"""
    try:
        if profile_service().change_password(request):
            return jsonify({"correct": "password changed"})
        return jsonify({"error": "bad password"}), 400
    except PasswordException:
        return jsonify({"error": "pass too short"}), 400
