from http import HTTPStatus

from config.limiter import limiter
from core.responses import (
    EMAIL_CHANGE,
    PASSWORD_CHANGE,
    PASSWORD_NOT_MATCH,
    PASSWORDS_EQUALS,
)
from core.schemas.profile_schemas import (
    EmailChangeReqeust,
    EmailChangeResponse,
    PasswordChangeReqeust,
    PasswordChangeResponse,
    PasswordEquals,
    PasswordNotMatch,
    ProfileResponse,
    UserLoginHistoryDeviceRequest,
    UserLoginHistoryDeviceResponse,
)
from core.spec_core import spec
from flask import Blueprint, request
from services.service_user_profile import profile_service, ProfileService
from services.tokens_service import token_required
from spectree import Response

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile.route("/", methods=["GET"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    resp=Response(HTTP_200=ProfileResponse),
    tags=["Profile"],
    security={"apiKey": []},
)
def user_full_information(service: ProfileService = profile_service()):
    """Ендпоинт для запроса данных пользователя"""
    token = request.headers.get("Authorization").split(" ")

    user_data = service.get_all_user_info(token[1])
    return ProfileResponse(**user_data)


@profile.route("/change/email", methods=["POST"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    json=EmailChangeReqeust,
    resp=Response(
        HTTP_200=EmailChangeResponse,
    ),
    tags=["Profile"],
    security={"apiKey": []},
)
def change_user_email(service: ProfileService = profile_service()):
    """Ендпоинт для изменения почтового адреса пользователя"""

    new_email = request.get_json().get("new_email")
    token = request.headers.get("Authorization").split(" ")
    service.change_email(token[1], new_email)
    return EmailChangeResponse(result=EMAIL_CHANGE), HTTPStatus.OK


@profile.route("/change/password", methods=["POST"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
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
def change_user_password(service: ProfileService = profile_service()):
    """Ендпоинт для изменения пароля пользователя"""

    user_data = request.get_json()
    password = user_data.get("password")
    new_password = user_data.get("new_password")

    if new_password == password:
        return PasswordEquals(result=PASSWORDS_EQUALS), HTTPStatus.BAD_REQUEST

    token = request.headers.get("Authorization").split(" ")
    if service.change_password(token[1], password, new_password):
        return PasswordChangeResponse(result=PASSWORD_CHANGE), HTTPStatus.OK
    return PasswordNotMatch(result=PASSWORD_NOT_MATCH), HTTPStatus.FORBIDDEN


@profile.route("/login/history", methods=["GET"])
@token_required()
@limiter.limit("10/second", override_defaults=False)
@spec.validate(
    query=UserLoginHistoryDeviceRequest,
    resp=Response(HTTP_200=UserLoginHistoryDeviceResponse),
    tags=["Profile"],
    security={"apiKey": []},
)
def user_login_history():
    """Ендпоинт для запроса данных пользователя"""
    token = request.headers.get("Authorization").split(" ")[1]
    page = request.args.get("page")
    page_size = request.args.get("page_size")
    if page is None:
        page = 1
    page = int(page)
    if page_size is None:
        page_size = 20
    page_size = int(page_size)
    login_history = profile_service().get_user_login_history(
        token, page, page_size
    )
    return UserLoginHistoryDeviceResponse(login_history=login_history)
