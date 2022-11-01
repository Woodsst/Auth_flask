from spectree import Response
from flask import Blueprint, request

from core.models import (spec, RouteResponse, EmailChangeReqeust,
                         PasswordChangeReqeust)
from services.service_user_profile import profile_service
from services.tokens_service import token_required
from core.responses import (
    PASSWORD_CHANGE,
    PASSWORDS_EQUALS,
    PASSWORD_NOT_MATCH,
    EMAIL_CHANGE,
    BAD_REQUEST,
)

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile.route("/", methods=["GET"])
@spec.validate(
    tags=["Profile"],
)
@token_required()
def user_full_information():
    """Ендпоинт для запроса данных пользователя"""
    token = request.headers.get("Authorization").split(" ")

    user_data = profile_service().get_all_user_info(token[1])
    return user_data


@profile.route("/devices/", methods=["GET"])
@profile.route(
    "/devices?page=<int:page>&page_size=<int:page_size>", methods=["GET"]
)
@token_required()
@spec.validate(
    tags=["Profile"],
)
def user_device_history():
    """Ендпоинт для запроса истории девайсов с которых была авторизация"""

    token = request.headers.get("Authorization").split(" ")
    page = request.args.get("page")
    if page is None or len(page) == 0:
        page = 1
    page = int(page)

    page_size = request.args.get("page_size")
    if page_size is None or len(page_size) == 0:
        page_size = 5
    page_size = int(page_size)

    user_devices_data = profile_service().get_devices_user_history(
        token[1], page, page_size
    )
    return user_devices_data


@profile.route("/change/email", methods=["POST"])
@spec.validate(
    json=EmailChangeReqeust,
    resp=Response(
        HTTP_200=RouteResponse, HTTP_400=RouteResponse, HTTP_401=RouteResponse
    ),
    tags=["Profile"],
)
@token_required()
def change_user_email():
    """Ендпоинт для изменения почтового адреса пользователя"""

    user_data = profile_service().data_exist(request)
    if not user_data:
        return RouteResponse(result=BAD_REQUEST), 400

    new_email = user_data.get("new_email")
    token = request.headers.get("Authorization").split(" ")
    profile_service().change_email(token[1], new_email)
    return RouteResponse(result=EMAIL_CHANGE), 200


@profile.route("/change/password", methods=["POST"])
@token_required()
@spec.validate(
    json=PasswordChangeReqeust,
    resp=Response(
        HTTP_200=RouteResponse, HTTP_400=RouteResponse, HTTP_401=RouteResponse
    ),
    tags=["Profile"],
)
def change_user_password():
    """Ендпоинт для изменения пароля пользователя"""

    user_data = profile_service().data_exist(request)
    if not user_data:
        return RouteResponse(result=BAD_REQUEST), 400

    password = user_data.get("password")
    new_password = user_data.get("new_password")

    if new_password == password:
        return RouteResponse(result=PASSWORDS_EQUALS), 400

    token = request.headers.get("Authorization").split(" ")
    if profile_service().change_password(token[1], password, new_password):
        return RouteResponse(result=PASSWORD_CHANGE), 200
    return RouteResponse(result=PASSWORD_NOT_MATCH), 400
