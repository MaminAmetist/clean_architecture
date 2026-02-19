from pydantic import BaseModel
from pydantic import ConfigDict


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
