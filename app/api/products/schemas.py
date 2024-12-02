from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, Field


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


class SearchProductSchema(BaseModel):
    q: Optional[Annotated[str, Field(min_length=4, max_length=30)]] = None


class FilterProductSchema(BaseModel):
    category_id: Optional[int] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
