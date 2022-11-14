from http import HTTPStatus

from flask import Response
from werkzeug.security import check_password_hash, generate_password_hash

from core.jaeger_tracer import d_trace
from core.jwt_api import (
    decode_access_token,
    generate_tokens,
    get_token_time_to_end,
)
from core.responses import PASSWORD_NOT_MATCH, USER_NOT_FOUND
from core.schemas.login_schemas import LoginPasswordNotMatch, LoginUserNotMatch
from core.spec_core import RouteResponse
from services.service_base import ServiceBase
from storages.postgres.db_models import LoginHistory, User


class LoginAPI(ServiceBase):
    def login(
        self,
        login: str,
        password: str,
        user_agent: str,
        is_pc: bool,
        login_ip: str,
    ) -> Response:
        """Проверка введенных данных пользователя"""

        try:
            user = User.query.filter_by(login=login).first()
            user_data = self._get_user_data(user.id)
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user_data.get("role")),
                }
                self._set_user_signin(user.id, is_pc, user_agent, login_ip)
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

    @d_trace
    def _set_user_signin(
        self, user_id: str, is_pc: bool, user_agent: str, login_ip: str
    ):
        """Добавляет информацию о входе пользователя"""
        if is_pc is True:
            device_type: str = "PC"
        else:
            device_type: str = "MOBILE"
        user_signin = LoginHistory(
            user_id=user_id,
            user_agent=user_agent,
            device_type=device_type,
            login_ip=login_ip,
        )

        self.orm.session.add(user_signin)
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

    def oauth_authentication(
        self,
        provider: str,
        login: str,
        password: str,
        email: str,
        user_agent: str,
        is_pc: str,
        login_ip: str,
    ):
        """Проверка существования пользователя по данным полученным от
        провайдера oauth, регистрация или аутентификация в зависимости от
        того, зарегистрирован пользователь или нет"""

        user = User.query.filter_by(login=login).first()
        if user:
            if check_password_hash(user.password, password):
                payload = {
                    "id": str(user.id),
                    "role": str(user.role),
                }
                return RouteResponse(result=generate_tokens(payload))
        self._set_user(
            {
                "login": login,
                "password": generate_password_hash(password),
                "email": email,
            }
        )
        self._set_social(login, provider, email)
        return self.login(login, password, user_agent, is_pc, login_ip)


def login_api():
    return LoginAPI()
