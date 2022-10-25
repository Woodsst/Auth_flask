from flask import Blueprint, request
from services.service_user_profile import profile_service

profile = Blueprint("profile", __name__, url_prefix="/api/v1")


@profile.route("/profile", methods=["GET"])
def user_full_information():
    user_data = profile_service().get_all_user_info(request)
    return user_data, 200


@profile.route("/profile/devices", methods=["GET"])
def user_device_history():
    user_devices_data = profile_service().get_devices_user_history(request)
    return user_devices_data, 200
