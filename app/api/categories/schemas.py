from pydantic import BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MaxLen, MinLen


class CreateCategorySchema(BaseModel):
    name: Annotated[str, MinLen(4), MaxLen(30)]


class CategorySchemaRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategorySchemaUpdate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
