from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int


class ProductSchemaRead(CreateProductSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateProductSchema(CreateProductSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
