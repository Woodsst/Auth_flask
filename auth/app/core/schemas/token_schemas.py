from pydantic import constr, BaseModel

from core.spec_core import RouteResponse
from core.responses import TOKEN_OUTDATED, ACCESS_DENIED


class TokenRequest(BaseModel):
    """access токен"""

    Authorization: constr(regex=r"(^Bearer\s[\w.\\w.\\w])")


class TokenOutDate(RouteResponse):
    """Схема ответа при истекшем токене"""

    class Config:
        schema_extra = {"example": TOKEN_OUTDATED}


class TokenAccessDenied(RouteResponse):
    """Схема ответа при запросе на администраторские станицы"""

    class Config:
        schema_extra = {"example": ACCESS_DENIED}
