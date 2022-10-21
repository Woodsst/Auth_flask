import json
from flask import Request
from services.service_base import ServiceBase
from storages.postgres.postgres_api import Postgres
from storages.postgres.alchemy_init import db


class Registration(ServiceBase):
    def registration(self, request: Request):
        user_data = json.loads(request.data)
        user_data['device'] = request.environ.get('HTTP_USER_AGENT')
        user_data['user']['role'] = 'user'
        user_data['user']['r_jwt'] = None
        self.db.set_user(user_data)


def registration():
    return Registration(Postgres(db))
