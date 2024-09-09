from fastapi import FastAPI, APIRouter
from src.db.database import engine
from src.models import mod_categories, mod_service
from src.endpoints import end_categories, end_service
from fastapi.middleware.cors import CORSMiddleware
from config import settings

mod_categories.Base.metadata.create_all(bind=engine) # alembikdan keyin ishlatish shart emas
mod_service.Base.metadata.create_all(bind=engine)


router = APIRouter()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    settings.cors_host,
    "http://localhost:3000",
]

app.add_middleware(

    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app. include_router(end_categories.router)
app. include_router(end_service.router)

@app.get("/")
def hello():
    return "hello"