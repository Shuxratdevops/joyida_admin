from pydantic import BaseModel
from src.schemas.sch_categories import CategoriesOut


class Base(BaseModel):
    name: str
    status: bool

class Service(Base):
    categories_id: int


class ServiceGet(Base):
    id: int
    category: CategoriesOut

