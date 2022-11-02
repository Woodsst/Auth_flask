from spectree import Response
from flask import Blueprint, request

from core.spec_core import spec
from core.schemas.profile_schemas import (
    DeviceRequest,
    DeviceResponse,
    ProfileResponse,
    EmailChangeResponse,
    EmailChangeReqeust,
    PasswordChangeReqeust,
    PasswordChangeResponse,
    PasswordEquals,
    PasswordNotMatch,
)
from services.service_user_profile import profile_service
from services.tokens_service import token_required
from core.responses import (
    PASSWORD_CHANGE,
    PASSWORDS_EQUALS,
    PASSWORD_NOT_MATCH,
    EMAIL_CHANGE,
)

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile.route("/devices", methods=["GET"])
@token_required()
@spec.validate(
    query=DeviceRequest,
    tags=["Profile"],
    resp=Response(HTTP_200=DeviceResponse),
    security={"apiKey": []},
)
def user_device_history():
    """Ендпоинт для запроса истории девайсов с которых была авторизация"""

    token = request.headers.get("Authorization").split(" ")
    page = int(request.args.get("page"))
    page_size = int(request.args.get("page_size"))

    user_devices_data = profile_service().get_devices_user_history(
        token[1], page, page_size
    )
    return DeviceResponse(history=user_devices_data)


@profile.route("/", methods=["GET"])
@token_required()
@spec.validate(
    resp=Response(HTTP_200=ProfileResponse),
    tags=["Profile"],
    security={"apiKey": []},
)
def user_full_information():
    """Ендпоинт для запроса данных пользователя"""
    token = request.headers.get("Authorization").split(" ")

    user_data = profile_service().get_all_user_info(token[1])
    return ProfileResponse(**user_data)


@profile.route("/change/email", methods=["POST"])
@token_required()
@spec.validate(
    json=EmailChangeReqeust,
    resp=Response(
        HTTP_200=EmailChangeResponse,
    ),
    tags=["Profile"],
    security={"apiKey": []},
)
def change_user_email():
    """Ендпоинт для изменения почтового адреса пользователя"""

    new_email = request.get_json().get("new_email")
    token = request.headers.get("Authorization").split(" ")
    profile_service().change_email(token[1], new_email)
    return EmailChangeResponse(result=EMAIL_CHANGE), 200


@profile.route("/change/password", methods=["POST"])
@token_required()
@spec.validate(
    json=PasswordChangeReqeust,
    resp=Response(
        HTTP_200=PasswordChangeResponse,
        HTTP_400=PasswordEquals,
        HTTP_403=PasswordNotMatch,
    ),
    tags=["Profile"],
    security={"apiKey": []},
)
def change_user_password():
    """Ендпоинт для изменения пароля пользователя"""

    user_data = request.get_json()
    password = user_data.get("password")
    new_password = user_data.get("new_password")

    if new_password == password:
        return PasswordEquals(result=PASSWORDS_EQUALS), 400

    token = request.headers.get("Authorization").split(" ")
    if profile_service().change_password(token[1], password, new_password):
        return PasswordChangeResponse(result=PASSWORD_CHANGE)
    return PasswordNotMatch(result=PASSWORD_NOT_MATCH), 403
