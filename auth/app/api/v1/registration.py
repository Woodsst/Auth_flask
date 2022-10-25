import email_validator
from exceptions import PasswordException
from flask import Blueprint, jsonify, request
from services.service_registration import registration_api
from exceptions import LoginException

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    try:
        response = registration_api().registration(request)
        if response:
            return jsonify("status: registration complete"), 201
        return jsonify({"error": "login or email already registered"}), 409
    except PasswordException:
        return jsonify({"error": "pass too short"}), 400
    except email_validator.EmailSyntaxError:
        return jsonify({"error": "The email address is not valid"}), 400
    except LoginException:
        return jsonify({"error": "login too short"}), 400
