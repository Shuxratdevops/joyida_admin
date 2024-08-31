from typing import Optional, List
from src.schemas import sch_service
from src.models import mod_service
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from src.db.database import get_db, engine


router = APIRouter(
    # prefix="/",
    tags=["service"]
)


@router.post("/service", status_code=status.HTTP_201_CREATED, response_model=sch_service.Service)
def create_service(service: sch_service.Service, db: Session = Depends(get_db)):
    new_service = mod_service.Service(**service.dict())

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.get("/service", response_model=List[sch_service.ServiceGet])
def get_service(db: Session = Depends(get_db)):
    service = db.query(mod_service.Service).all()

    return service


@router.get("/service/{id}", response_model=sch_service.Service)
def get_service(id: int, db: Session = Depends(get_db)):
    service = db.query(mod_service.Service).filter(mod_service.Service.id == id).first()

    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return service


@router.put("/service/{id}", response_model=sch_service.Service)
def update_service(id: int, updated_service: sch_service.Service, db: Session = Depends(get_db)):

    service_query = db.query(mod_service.Service).filter(mod_service.Service.id == id)
    service = service_query.first()

    if service == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    service_query.update(updated_service.dict(), synchronize_session=False)

    db.commit()
    return service_query.first()


@router.delete("/service/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(id: int, db: Session = Depends(get_db)):

    service_query = db.query(mod_service.Service).filter(mod_service.Service.id == id)
    service = service_query.first()

    if service == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    service_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)