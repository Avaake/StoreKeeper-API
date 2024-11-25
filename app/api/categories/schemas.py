from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional, List
from annotated_types import MaxLen, MinLen


class CreateCategorySchema(BaseModel):
    name: Annotated[str, MinLen(4), MaxLen(30)]


class CategorySchemaRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryListRead(BaseModel):
    categories: List[CategorySchemaRead]


class CategorySchemaUpdate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
