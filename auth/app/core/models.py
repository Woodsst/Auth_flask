from pydantic import BaseModel, constr, EmailStr, validator
from spectree import SpecTree

spec = SpecTree("flask")


class RegistrationReqeust(BaseModel):
    """Тело запроса для регистрации"""

    login: constr(min_length=2, max_length=36)
    password: constr(min_length=8, max_length=36)
    email: EmailStr


class LoginRequest(BaseModel):
    """Тело запроса для аутентификации"""
    login: str
    password: str


class RouteResponse(BaseModel):
    result: dict


class Logout(BaseModel):
    Authorization: str

    @validator('Authorization')
    def header_valid(cls, value: str):
        if value.split(" ") != 2:
            return ValueError()
        return value.title()
