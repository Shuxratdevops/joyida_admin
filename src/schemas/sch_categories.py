from pydantic import BaseModel


class Categories(BaseModel):
    name: str
    status: bool


class CategoriesGet(Categories):
    id: int


class CategoriesOut(BaseModel):
    id: int
    name: str