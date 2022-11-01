from pydantic import BaseModel
from spectree import SpecTree

spec = SpecTree("flask")


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
