import uuid

from flask import jsonify, make_response, Response
from services.service_base import ServiceBase
from storages.postgres.db_models import User, Device, UserDevice
from werkzeug.security import check_password_hash
from jwt_api import get_token_time_to_end
from core.responses import USER_NOT_FOUND, PASSWORD_NOT_MATCH


class LoginAPI(ServiceBase):
    def login(self, login: str, password: str, user_agent: str) -> Response:
        try:
            user = User.query.filter_by(login=login).first()
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user.role),
                }
                self._set_device(user_agent, user.id)
                return self.generate_tokens(payload)
            responseObject = PASSWORD_NOT_MATCH
            return make_response(jsonify(responseObject)), 401
        except AttributeError:
            responseObject = USER_NOT_FOUND
            return make_response(jsonify(responseObject)), 401

    def _set_device(self, device: str, user_id: str):
        """Добавление нового устройства с которого клиент зашел в аккаунт"""

        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.add(device)
        self.orm.add(user_device)
        self.orm.commit()

    def logout(self, access_token: str):
        """Записывает токен в базу как невалидный"""
        time_to_end = get_token_time_to_end(access_token)
        if time_to_end:
            self.cash.set_token(key=access_token, value=1, exited=time_to_end)
            return True
        return False


def login_api():
    return LoginAPI()
