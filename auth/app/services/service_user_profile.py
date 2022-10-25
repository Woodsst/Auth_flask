import json

from services.service_base import ServiceBase
from storages.db_connect import db
from storages.postgres.postgres_api import Postgres
from flask import Request
from jwt_api import decode_access_token


class ProfileService(ServiceBase):
    def get_all_user_info(self, request: Request):
        token = request.headers.get("Authorization").split(" ")[1]
        user_id = decode_access_token(token).get("id")

        user_data = self.db.get_user_data(user_id)
        return self.format_user_data(user_data)

    @staticmethod
    def format_user_data(user_data: dict) -> dict:
        role = user_data.get("role").value
        return json.dumps(
            {
                "login": user_data.get("login"),
                "email": user_data.get("email"),
                "role": role,
            }
        )


def profile_service():
    return ProfileService(Postgres(db))
