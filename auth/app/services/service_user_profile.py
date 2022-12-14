from typing import Union, Optional

import werkzeug.exceptions
from werkzeug.security import generate_password_hash

from core.jaeger_tracer import d_trace
from core.jwt_api import get_user_id_from_token
from services.service_base import ServiceBase
from storages.postgres.db_models import (
    LoginHistory,
    User,
)


class ProfileService(ServiceBase):
    def get_all_user_info(self, token: str) -> dict:
        """Получение данных пользователя"""

        user_id = get_user_id_from_token(token)

        user_data = self._get_user_data(user_id)
        return self._format_user_data(user_data)

    @staticmethod
    def _format_user_data(user_data: dict) -> dict:
        """Форматирование данных из базы для отправки пользователю"""

        role = user_data.get("role")
        user_data = user_data.get("User").to_dict()
        return {
            "login": user_data.get("login"),
            "email": user_data.get("email"),
            "role": role,
        }

    def get_user_login_history(
        self, token: str, page: int, page_size: int
    ) -> Union[dict, list]:
        """Получение устройств с которых входили в профиль"""

        user_id = get_user_id_from_token(token)
        raw_login_history_class = self._get_user_login_history(
            user_id, page, page_size
        )
        if raw_login_history_class is not None:
            return self._format_user_login_history(raw_login_history_class)
        return []

    @staticmethod
    def _format_user_login_history(raw_login_history_class: list) -> dict:
        """Форматирование данных истории входов пользователя"""
        login_history_list = []
        for item in raw_login_history_class:
            login_history_dict = item.to_dict()
            login_history_dict["device_type"] = item.device_type.value
            del login_history_dict["event_type"]
            del login_history_dict["id"]
            login_history_list.append(login_history_dict)
        return login_history_list

    def change_email(self, token: str, new_email: str):
        """Изменение почты пользователя"""

        user_id = get_user_id_from_token(token)
        self._change_user_email(user_id, new_email)

    def change_password(
        self, token: str, password: str, new_password: str
    ) -> bool:
        """Изменение пароля пользователя"""

        user_id = get_user_id_from_token(token)

        if self.check_password(password, user_id):
            new_password = generate_password_hash(new_password)
            self._change_user_password(user_id, new_password)
            return True
        return False

    @d_trace
    def _change_user_email(self, user_id: str, email: str):
        """Запрос в базу для изменения почты клиента"""

        self.orm.session.query(User).filter(User.id == user_id).update(
            {"email": email}, synchronize_session="fetch"
        )
        self.orm.session.commit()

    @d_trace
    def _change_user_password(self, user_id, password: str):
        """Запрос в базу для изменения пароля клиента"""

        self.orm.session.query(User).filter(User.id == user_id).update(
            {"password": password}, synchronize_session="fetch"
        )
        self.orm.session.commit()

    @d_trace
    def _get_user_login_history(
        self, user_id: str, page: int, page_size: int
    ) -> Optional[list]:
        """Получение истории входов пользователя"""
        try:
            login_history = (
                self.orm.session.query(LoginHistory)
                .filter(User.id == user_id)
                .paginate(page=page, per_page=page_size, count=False)
            )
            return login_history
        except werkzeug.exceptions.NotFound:
            return


def profile_service():
    return ProfileService()
