import uuid
from http import HTTPStatus
from urllib.parse import urlencode

from flask import Response
from requests import post, get
from werkzeug.security import check_password_hash, generate_password_hash

from config.settings import settings
from core.schemas.login_schemas import LoginPasswordNotMatch, LoginUserNotMatch
from core.spec_core import (
    RouteResponse,
)
from core.responses import USER_NOT_FOUND, PASSWORD_NOT_MATCH
from jwt_api import (
    get_token_time_to_end,
    generate_tokens,
    decode_access_token,
    decode_yandex_jwt,
)
from services.service_base import ServiceBase
from storages.postgres.db_models import User, Device, UserDevice


class LoginAPI(ServiceBase):
    def login(self, login: str, password: str, user_agent: str) -> Response:
        """Проверка введенных данных пользователя"""

        try:
            user = User.query.filter_by(login=login).first()
            user_data = self._get_user_data(user.id)
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user_data.get("role")),
                }
                self._set_device(user_agent, user.id)
                return RouteResponse(result=generate_tokens(payload))
            return (
                LoginPasswordNotMatch(result=PASSWORD_NOT_MATCH),
                HTTPStatus.FORBIDDEN,
            )
        except AttributeError:
            return (
                LoginUserNotMatch(result=USER_NOT_FOUND),
                HTTPStatus.UNAUTHORIZED,
            )

    def _set_device(self, device: str, user_id: str):
        """Добавление нового устройства с которого клиент зашел в аккаунт"""

        id = uuid.uuid4()
        device = Device(id=id, device=device)
        user_device = UserDevice(device_id=id, user_id=user_id)
        self.orm.session.add(device)
        self.orm.session.add(user_device)
        self.orm.session.commit()

    def logout(self, access_token: str):
        """Записывает access и refresh токены в базу как невалидные"""

        access_time_to_end = get_token_time_to_end(access_token)
        if access_time_to_end:
            refresh = decode_access_token(access_token).get("refresh")
            refresh_time_to_end = get_token_time_to_end(refresh)
            self.cash.set_token(
                key=refresh, value=1, exited=refresh_time_to_end
            )
            self.cash.set_token(
                key=access_token, value=1, exited=access_time_to_end
            )
            return True
        return False

    def oauth(self, tokens: dict, user_agent: str):
        """Получение данных о пользователе от yandex,
        регистрация нового пользователя если его нет,
        или авторизация если он уже зарегистрирован"""

        client_jwt = get(
            "https://login.yandex.ru/info?format=jwt",
            headers={"Authorization": f"Oauth {tokens.get('access_token')}"},
        )

        client_info = decode_yandex_jwt(client_jwt.content.decode())
        login = client_info.get("login")
        password = client_info.get("psuid")
        user = User.query.filter_by(login=login).first()
        if user:
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user.role),
                }
                self._set_device(user_agent, user.id)
                return RouteResponse(result=generate_tokens(payload))
        self._set_user(
            {
                "login": login,
                "password": generate_password_hash(password),
                "email": client_info.get("email"),
            }
        )
        self._set_social(login, "Yandex", client_info.get("email"))
        return self.login(login, password, user_agent)

    @staticmethod
    def get_tokens(code: str):
        """Получение токенов доступа к информации о пользователе"""

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.yandex_client_id,
            "client_secret": settings.yandex_client_secret,
        }
        data = urlencode(data)
        tokens = post(f"{settings.yandex_baseurl}token", data)
        tokens = tokens.json()
        return tokens


def login_api():
    return LoginAPI()
