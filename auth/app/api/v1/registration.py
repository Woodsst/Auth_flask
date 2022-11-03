import json
from http import HTTPStatus

from core.responses import REGISTRATION_COMPLETE, REGISTRATION_FAILED
from core.schemas.registration_schemas import (
    RegistrationFailed,
    RegistrationReqeust,
)
from core.spec_core import RouteResponse, spec
from flask import Blueprint, request
from services.service_registration import registration_api
from spectree import Response

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
@spec.validate(
    json=RegistrationReqeust,
    resp=Response(HTTP_201=RouteResponse, HTTP_409=RegistrationFailed),
    tags=["Registration"],
)
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    user_data = json.loads(request.data)
    response = registration_api().registration(user_data)

    if response:
        return RouteResponse(result=REGISTRATION_COMPLETE), HTTPStatus.CREATED

    return RegistrationFailed(result=REGISTRATION_FAILED), HTTPStatus.CONFLICT
