from pydantic import BaseModel, constr, EmailStr

from core.spec_core import RouteResponse
from core.responses import REGISTRATION_FAILED


class RegistrationReqeust(BaseModel):
    """Тело запроса для регистрации"""

    login: constr(min_length=2, max_length=36)
    password: constr(min_length=8, max_length=36)
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "login": "login",
                "password": "password",
                "email": "email@email.com",
            }
        }


class RegistrationFailed(RouteResponse):
    """Схема ошибки при регистрации"""

    class Config:
        schema_extra = {"example": REGISTRATION_FAILED}
