from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen


class AuthCreateUser(BaseModel):
    username: Optional[Annotated[str, MinLen(4), MaxLen(30)]] = None
    email: EmailStr
    password: Annotated[str, MinLen(5), MaxLen(30)]


class BaseUser(BaseModel):
    username: Optional[Annotated[str, MinLen(4), MaxLen(30)]] = None
    email: EmailStr
    role: str


class CreateUser(BaseUser):
    password: str


class UserRead(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseUser):
    username: Optional[Annotated[str, MinLen(4), MaxLen(30)]] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
