from pydantic import BaseModel, constr, EmailStr
from spectree import SpecTree

spec = SpecTree("flask")


class RegistrationReqeust(BaseModel):
    login: constr(min_length=2, max_length=36)
    password: constr(min_length=8, max_length=36)
    email: EmailStr


class RegistrationResponse(BaseModel):
    result: dict
