from typing import Optional

from pydantic import BaseModel, conint, EmailStr, constr

from core.spec_core import RouteResponse
from core.responses import (
    EMAIL_CHANGE,
    PASSWORD_CHANGE,
    PASSWORDS_EQUALS,
    PASSWORD_NOT_MATCH,
)


class ProfileResponse(BaseModel):
    """Схемат ответа при запросе данных пользователя"""

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

    page: Optional[conint(gt=0)] = None
    page_size: Optional[conint(gt=0)] = None


class DeviceResponse(BaseModel):
    """Схема ответа при запросе истории устройств
    с которых был вход в профиль"""

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
