from services.service_base import ServiceBase
from werkzeug.security import generate_password_hash


class Registration(ServiceBase):
    def registration(self, user_data: dict) -> dict:
        """Хеширование пароля и добавление нового пользователя"""

        user_data["password"] = generate_password_hash(user_data["password"])
        return self._set_user(user_data)


def registration_api():
    return Registration()
