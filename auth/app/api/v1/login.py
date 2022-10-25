from flask import Blueprint, request
from auth.app.services.login_service import login_api

login_page = Blueprint(
    "login_page", __name__, url_prefix="/api/v1"
)


@login_page.route("/login", methods=["POST"])
def registration_user():
    response = login_api().login(request)
    return response
