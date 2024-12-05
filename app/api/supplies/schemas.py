from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum


class StatusListSchema(str, Enum):
    pending = "pending"
    delivery = "delivery"
    cancelled = "cancelled"


class BaseSupplySchema(BaseModel):
    product_name: Annotated[str, Field(min_length=5, max_length=255)]
    quantity: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(gt=0)]
    supplier_id: Annotated[int, Field(gt=0)]
    delivery_date: datetime
    status: StatusListSchema


class CreateSupplySchema(BaseSupplySchema):
    pass


class ReadSupplySchema(BaseSupplySchema):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateSupplySchema(BaseSupplySchema):
    product_name: Optional[Annotated[str, Field(min_length=5, max_length=255)]] = None
    quantity: Optional[Annotated[int, Field(gt=0)]] = None
    price: Optional[Annotated[float, Field(gt=0)]] = None
    supplier_id: Optional[Annotated[int, Field(gt=0)]] = None
    delivery_date: Optional[datetime] = None
    status: Optional[StatusListSchema] = None
