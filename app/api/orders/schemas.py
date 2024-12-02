from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class OrderItemCrateSchema(BaseModel):
    product_id: int
    quantity: int = Field(
        ..., ge=1, description="Кількість товару, має бути більше або дорівнювати 1"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"product_id": 1, "quantity": 3}},
        from_attributes=True,
    )


class OrderCreateSchema(BaseModel):
    products: List[OrderItemCrateSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "products": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1},
                ]
            }
        },
    )


class OrderItemsRead(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class StatusListSchema(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class OrderItemUpdateSchema(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = Field(
        None, ge=1, description="Кількість товару, має бути більше або дорівнювати 1"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"product_id": 1, "quantity": 3}},
        from_attributes=True,
    )


class OrderUpdateSchema(BaseModel):
    status: Optional[StatusListSchema] = None
    products: Optional[List[OrderItemUpdateSchema]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "status": "completed",
                "products": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1},
                ],
            }
        },
    )


from datetime import datetime


class FilterOrderSchema(BaseModel):
    status: Optional[StatusListSchema] = None
    start_day: Optional[datetime] = None
    end_day: Optional[datetime] = None
