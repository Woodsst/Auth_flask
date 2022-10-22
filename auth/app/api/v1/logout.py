from flask import Blueprint, request
from services.service_registration import registration

registration_page = Blueprint("registration_page",
                              __name__,
                              url_prefix="/api/v1")


@registration_page.route("/registration", methods=["POST"])
def registration_user():
    registration().registration(request)
    return "Hello, registration!"
