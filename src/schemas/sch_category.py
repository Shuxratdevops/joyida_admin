from pydantic import BaseModel


class Category(BaseModel):
    name: str
    status: bool


class CategoryGet(Category):
    id: int