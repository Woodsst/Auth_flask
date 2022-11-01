import uuid

from pydantic import BaseModel, constr

from core.spec_core import RouteResponse
from core.responses import ROLE_EXISTS, ROLE_NOT_EXIST, DEFAULT_ROLE_NOT_DELETE


class AddRoleRequest(BaseModel):
    """Схема для добавления роли"""

    role: constr(min_length=2)
    description: constr(min_length=2)

    class Config:
        schema_extra = {
            "example": {
                "role": "new role",
                "description": "new description",
            }
        }


class AddRoleExist(RouteResponse):
    class Config:
        schema_extra = {"example": ROLE_EXISTS}


class DeleteRoleRequest(BaseModel):
    """Схема для удаления роли"""

    role: str


class DeleteRoleNotExist(RouteResponse):
    class Config:
        schema_extra = {"example": ROLE_NOT_EXIST}


class DeleteRoleDefaultRole(RouteResponse):
    class Config:
        schema_extra = {"example": DEFAULT_ROLE_NOT_DELETE}


class ChangeRoleRequest(BaseModel):
    """Схема для изменения роли"""

    role: constr(min_length=2)
    change_description: str
    change_role: constr(min_length=2)

    class Config:
        schema_extra = {
            "example": {
                "role": "role",
                "change_description": "change_description",
                "change_role": "change_role",
            }
        }


class UserRoleRequest(BaseModel):
    """Схема для изменения роли у пользователя"""

    user_id: uuid.UUID
    role: constr(min_length=2)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "role",
            }
        }
