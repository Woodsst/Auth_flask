import uuid

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
