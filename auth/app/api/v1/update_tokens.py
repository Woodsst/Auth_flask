from flask import Blueprint


update = Blueprint("update", __name__, url_prefix="/api/v1")


@update.route("/token", methods=["GET"])
def registration_user():
    pass
