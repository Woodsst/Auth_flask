import json

from flask import Blueprint, request
from spectree import Response

from core.models import RegistrationReqeust, RouteResponse, spec
from core.responses import (
    REGISTRATION_COMPLETE,
    REGISTRATION_FAILED,
)
from services.service_registration import registration_api

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
@spec.validate(
    json=RegistrationReqeust,
    resp=Response(HTTP_201=RouteResponse, HTTP_409=RouteResponse),
    tags=["Registration"],
)
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    user_data = json.loads(request.data)
    response = registration_api().registration(user_data)

    if response:
        return RouteResponse(result=REGISTRATION_COMPLETE), 201

    return RouteResponse(result=REGISTRATION_FAILED), 409
