from pydantic import BaseModel
from spectree import SpecTree


class SecuritySchema(BaseModel):
    name: str
    data: dict


spec = SpecTree(
    "flask",
    security_schemes=[
        SecuritySchema(
            name="apiKey",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
)


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
