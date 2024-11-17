from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen


class CreateUser(BaseModel):
    username: Optional[Annotated[str, MinLen(4), MaxLen(30)]] = None
    email: EmailStr
    password: str
