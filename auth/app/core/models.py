from pydantic import BaseModel, constr, EmailStr
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


class BearerToken(BaseModel):
    Authorization: constr(regex=r"(^Bearer\s[\w.\\w.\\w])")


class EmailChangeReqeust(BaseModel):
    """Тело запроса для изменения почтового адреса пользователя"""

    new_email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "message": "email changed",
                    "status": "succeeded"
                }
            }
        }


class PasswordChangeReqeust(BaseModel):
    """Тело запроса для изменения пароля пользователя"""

    password: str
    new_password: constr(min_length=8, max_length=36)

    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "message": "password changed",
                    "status": "succeeded"
                }
            }
        }
