import uuid

from pydantic import BaseModel, constr, EmailStr, conint
from spectree import SpecTree

from core.responses import (
    EMAIL_CHANGE,
    PASSWORD_CHANGE,
    PASSWORDS_EQUALS,
    PASSWORD_NOT_MATCH,
)

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
    """Схемат ответа"""

    result: dict

    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "status": "succeeded",
                    "message": "request completed",
                }
            }
        }


class ProfileResponse(BaseModel):
    """Схемат ответа"""

    login: str
    email: str
    role: str

    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "login": "login",
                    "role": "User",
                    "email": "email@email.com",
                }
            }
        }


class DeviceRequest(BaseModel):
    """Схема запроса списка устройств с которых был вход в профиль"""

    page: conint(gt=0)
    page_size: conint(gt=0)


class DeviceResponse(BaseModel):
    history: list[dict]

    class Config:
        schema_extra = {
            "example": {
                "history": [
                    {
                        "device": "some device",
                        "entry_time": "2022-11-01 15:45:44.946777",
                    },
                    {
                        "device": "some new device",
                        "entry_time": "2022-11-01 15:45:44.946777",
                    },
                ]
            }
        }


class Token(BaseModel):
    """access токен"""

    Authorization: constr(regex=r"(^Bearer\s[\w.\\w.\\w])")


class AddRole(BaseModel):
    """Схема для добавления роли"""

    role: constr(min_length=2)
    description: constr(min_length=2)


class DeleteRole(BaseModel):
    """Схема для удаления роли"""

    role: str


class ChangeRole(BaseModel):
    """Схема для изменения роли"""

    role: constr(min_length=2)
    change_description: str
    change_role: constr(min_length=2)


class UserRole(BaseModel):
    """Схема для изменения роли у пользователя"""

    user_id: uuid.UUID
    role: constr(min_length=2)


class EmailChangeReqeust(BaseModel):
    """Схема запроса для изменения почтового адреса пользователя"""

    new_email: EmailStr

    class Config:
        schema_extra = {"example": {"new_email": "new@email.com"}}


class EmailChangeResponse(RouteResponse):
    """Схема ответа для изменения почтового адреса пользователя"""

    class Config:
        schema_extra = {"example": {"result": EMAIL_CHANGE}}


class PasswordChangeReqeust(BaseModel):
    """Схема запроса для изменения пароля пользователя"""

    password: str
    new_password: constr(min_length=8, max_length=36)

    class Config:
        schema_extra = {
            "example": {
                "password": "old password",
                "new_password": "new password",
            }
        }


class PasswordChangeResponse(RouteResponse):
    """Схема ответа на успешное изменение пароля"""

    class Config:
        schema_extra = {"example": {"result": PASSWORD_CHANGE}}


class PasswordEquals(PasswordChangeResponse):
    """Схема ответа на повторяющиеся пароли"""

    class Config:
        schema_extra = {"example": {"result": PASSWORDS_EQUALS}}


class PasswordNotMatch(PasswordChangeResponse):
    """Схема ответа на неправильный пароль"""

    class Config:
        schema_extra = {"example": {"result": PASSWORD_NOT_MATCH}}
