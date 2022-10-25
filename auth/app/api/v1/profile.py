import email_validator
from flask import Blueprint, request, jsonify
from services.service_user_profile import profile_service

profile = Blueprint("profile", __name__, url_prefix="/api/v1")


@profile.route("/profile", methods=["GET"])
def user_full_information():
    user_data = profile_service().get_all_user_info(request)
    return user_data


@profile.route("/profile/devices", methods=["GET"])
def user_device_history():
    user_devices_data = profile_service().get_devices_user_history(request)
    return user_devices_data


@profile.route("/profile/socials", methods=["GET"])
def user_socials():
    user_socials_data = profile_service().get_socials(request)
    return user_socials_data


@profile.route("/profile/change/email", methods=["POST"])
def change_user_email():
    try:
        profile_service().change_email(request)
        return jsonify({"correct": "email changed"})
    except email_validator.EmailSyntaxError:
        return jsonify({"error": "The email address is not valid"}), 400
