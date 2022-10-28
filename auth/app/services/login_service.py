from functools import lru_cache

from flask import jsonify, make_response
from services.service_base import ServiceBase
from storages.postgres.db_models import User
from werkzeug.security import check_password_hash
from jwt_api import get_token_time_to_end


class LoginAPI(ServiceBase):
    def login(self, login: str, password: str):
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
                "message": "the password does not match the user's password",
            }
            return make_response(jsonify(responseObject)), 401
        except AttributeError:
            responseObject = {
                "status": "fail",
                "message": (
                    "The user with such login and password was not" "found"
                ),
            }
            return make_response(jsonify(responseObject)), 403

    def logout(self, access_token: str):
        """Записывает токен в базу как невалидный"""

        time_to_end = get_token_time_to_end(access_token)
        self.cash.set_token(key=access_token, value=1, exited=time_to_end)


@lru_cache()
def login_api():
    return LoginAPI()
