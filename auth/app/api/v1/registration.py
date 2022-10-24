import email_validator
from flask import Blueprint, request, jsonify
from services.service_registration import registration_api
from exceptions import PasswordException

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
def registration_user():
    try:
        response = registration_api().registration(request)
        if response:
            return jsonify("status: registration complete"), 201
        else:
            return jsonify({"error": "login or email already registered"}), 409
    except PasswordException:
        return jsonify({"error": "pass too short"}), 403
    except email_validator.EmailSyntaxError:
        return jsonify({"error": "The email address is not valid"}), 403
    except ValueError:
        return jsonify({"error": "login too short"}), 403