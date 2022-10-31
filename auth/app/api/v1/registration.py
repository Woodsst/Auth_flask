import json

from flask import Blueprint, request
from services.service_registration import registration_api
from core.responses import (
    REGISTRATION_COMPLETE,
    REGISTRATION_FAILED,
)
from core.models import RegistrationReqeust, RegistrationResponse, spec
from spectree import Response

registration_page = Blueprint(
    "registration_page", __name__, url_prefix="/api/v1"
)


@registration_page.route("/registration", methods=["POST"])
@spec.validate(
    json=RegistrationReqeust,
    resp=Response(
        HTTP_201=RegistrationResponse, HTTP_409=RegistrationResponse
    ),
)
def registration_user():
    """Ендпоинт регистрации клиента, принимает POST запрос с данными клиента
    в теле запроса"""
    user_data = json.loads(request.data)
    response = registration_api().registration(user_data)

    if response:
        return RegistrationResponse(result=REGISTRATION_COMPLETE), 201

    return RegistrationResponse(result=REGISTRATION_FAILED), 409
