import uuid

from flask import jsonify, make_response, Response

from core.models import RouteResponse
from services.service_base import ServiceBase
from storages.postgres.db_models import User, Device, UserDevice
from werkzeug.security import check_password_hash
from jwt_api import get_token_time_to_end, generate_tokens
from core.responses import USER_NOT_FOUND, PASSWORD_NOT_MATCH


class LoginAPI(ServiceBase):
    def login(self, login: str, password: str, user_agent: str) -> Response:
        """Проверка введенных данных пользователя"""

        try:
            user = User.query.filter_by(login=login).first()
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user.role),
                }
                self._set_device(user_agent, user.id)
                return RouteResponse(result=generate_tokens(payload))
            return RouteResponse(result=PASSWORD_NOT_MATCH), 401
        except AttributeError:
            return RouteResponse(result=USER_NOT_FOUND), 401

    def _set_device(self, device: str, user_id: str):
        """Добавление нового устройства с которого клиент зашел в аккаунт"""

        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.session.add(device)
        self.orm.session.add(user_device)
        self.orm.session.commit()

    def logout(self, access_token: str):
        """Записывает токен в базу как невалидный"""
        time_to_end = get_token_time_to_end(access_token)
        if time_to_end:
            self.cash.set_token(key=access_token, value=1, exited=time_to_end)
            return True
        return False


def login_api():
    return LoginAPI()
