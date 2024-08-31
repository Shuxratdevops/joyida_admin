from fastapi import FastAPI, APIRouter
from src.db.database import engine
from src.models import mod_category, mod_service
from src.endpoints import end_category, end_service

mod_category.Base.metadata.create_all(bind=engine) # alembikdan keyin ishlatish shart emas
mod_service.Base.metadata.create_all(bind=engine)


router = APIRouter()

app = FastAPI()


app. include_router(end_category.router)
app. include_router(end_service.router)