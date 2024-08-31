from pydantic import BaseModel


class Service(BaseModel):
    name: str
    category_id: int
    status: bool

class ServiceGet(Service):
    id: int