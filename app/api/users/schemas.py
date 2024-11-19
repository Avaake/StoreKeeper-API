from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional, List
from annotated_types import MaxLen, MinLen


class AuthCreateUser(BaseModel):
    username: Optional[Annotated[str, MinLen(4), MaxLen(30)]] = None
    email: EmailStr
    password: str
