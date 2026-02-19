from pydantic import BaseModel
from pydantic import ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    category_id: int


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
