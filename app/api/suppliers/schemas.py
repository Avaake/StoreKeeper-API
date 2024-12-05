from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, Annotated


class BaseSupplierSchema(BaseModel):
    name: Annotated[str, Field(min_length=5, max_length=255)]
    email: Optional[EmailStr] = None
    phone_number: Optional[Annotated[str, Field(min_length=9, max_length=13)]] = None
    address: Optional[Annotated[str, Field(min_length=5, max_length=255)]] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        return value


class CreateSupplierSchema(BaseSupplierSchema):
    model_config = ConfigDict(from_attributes=True)


class ReadSupplierSchema(BaseSupplierSchema):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class SearchSupplierSchema(BaseModel):
    q: Optional[Annotated[str, Field(min_length=3, max_length=100)]] = None


class UpdateSupplierSchema(BaseSupplierSchema):
    name: Optional[str] = Field(None, min_length=5, max_length=255)
