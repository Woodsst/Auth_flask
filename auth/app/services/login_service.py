from flask import Request, jsonify, make_response
from services.service_base import ServiceBase
from storages.db_connect import db, redis_conn
from storages.postgres.db_models import User
from storages.postgres.postgres_api import Postgres
from storages.redis.redis_api import Redis
from werkzeug.security import check_password_hash


class LoginAPI(ServiceBase):
    def login(self, request: Request):
        data = request.get_json()
        login = data.get("login")
        password = data.get("password")
        try:
            user = User.query.filter_by(login=login).first()
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user.role),
                }
                return self.generate_tokens(payload)
            responseObject = {
                "status": "fail",
                "message": "the password does not match the user's password"
            }
            return make_response(jsonify(responseObject)), 401
        except AttributeError:
            responseObject = {
                "status": "fail",
                "message": ("The user with such login and password was not"
                            "found")
            }
            return make_response(jsonify(responseObject)), 403


def login_api():
    return LoginAPI(Postgres(db), Redis(redis_conn))
