from flask import Blueprint, request, jsonify
from services.service_registration import registration_api

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
def registration_user():
    tokens = registration_api().registration(request)
    if tokens:
        return tokens, 201
    else:
        return jsonify("error: login or email already registered"), 409
