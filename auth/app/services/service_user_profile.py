import json

from services.service_base import ServiceBase
from storages.db_connect import db
from storages.postgres.postgres_api import Postgres
from flask import Request


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
        history = self.format_devices_history(raw_history)
        return history

    @staticmethod
    def format_devices_history(raw_history: list) -> dict:
        history = []
        for entry in raw_history:
            entry = entry._asdict()
            entry_time = entry.get("entry_time")
            entry["entry_time"] = str(entry_time)
            history.append(entry)
        return history


def profile_service():
    return ProfileService(Postgres(db))
