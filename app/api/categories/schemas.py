from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional, List
from annotated_types import MaxLen, MinLen


class CreateCategorySchema(BaseModel):
    name: str


class CategorySchemaRead(BaseModel):
    id: Optional[int] = None
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryListRead(BaseModel):
    categories: List[CategorySchemaRead]
