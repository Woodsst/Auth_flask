from pydantic import BaseModel

from core.spec_core import RouteResponse
from core.responses import PASSWORD_NOT_MATCH, USER_NOT_FOUND


class LoginRequest(BaseModel):
    """Тело запроса для аутентификации"""

    login: str
    password: str


class LoginPasswordNotMatch(RouteResponse):
    """Схема ответа при неверном пароле"""

    class Config:
        schema_extra = {"example": PASSWORD_NOT_MATCH}


class LoginUserNotMatch(RouteResponse):
    """Схема ответа при неправильном логине"""

    class Config:
        schema_extra = {"example": USER_NOT_FOUND}
