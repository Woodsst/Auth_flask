import json

from services.service_base import ServiceBase
from storages.db_connect import db_session
from storages.postgres.postgres_api import Postgres
from flask import Request
from email_validator import validate_email
from werkzeug.security import generate_password_hash

from exceptions import PasswordException


class ProfileService(ServiceBase):
    def get_all_user_info(self, request: Request):
        user_id = self.get_user_id_from_token(request)

        user_data = self.db.get_user_data(user_id)
        return self._format_user_data(user_data)

    @staticmethod
    def _format_user_data(user_data: dict) -> dict:
        role = user_data.get("role").value
        return json.dumps(
            {
                "login": user_data.get("login"),
                "email": user_data.get("email"),
                "role": role,
            }
        )

    def get_devices_user_history(self, request: Request):
        user_id = self.get_user_id_from_token(request)
        raw_history = self.db.get_user_device_history(user_id)
        history = self._format_devices_history(raw_history)
        return history

    @staticmethod
    def _format_devices_history(raw_history: list) -> dict:
        history = []
        for entry in raw_history:
            entry = entry._asdict()
            entry_time = entry.get("entry_time")
            entry["entry_time"] = str(entry_time)
            history.append(entry)
        return history

    def get_socials(self, request):
        user_id = self.get_user_id_from_token(request)
        social = self.db.get_user_social(user_id)
        return social

    def change_email(self, request: Request):
        user_data = json.loads(request.data)
        new_email = user_data.get("new_email")
        validate_email(new_email)
        user_id = self.get_user_id_from_token(request)
        self.db.change_user_email(user_id, new_email)

    def change_password(self, request: Request):
        user_id = self.get_user_id_from_token(request)
        user_data = json.loads(request.data)
        password = user_data.get("password")
        new_password = user_data.get("new_password")

        if len(new_password) < 8:
            raise PasswordException("password too short")

        if self.check_password(password, user_id):
            if new_password == password:
                return False
            new_password = generate_password_hash(new_password)
            self.db.change_user_password(user_id, new_password)
            return True
        return False


def profile_service():
    return ProfileService(Postgres(db_session))
