from typing import Optional, List
from src.schemas import sch_category
from src.models import mod_category
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from src.db.database import get_db, engine


router = APIRouter(
    # prefix="/",
    tags=["category"]
)


@router.post("/category", status_code=status.HTTP_201_CREATED, response_model=sch_category.Category)
def create_category(category: sch_category.Category, db: Session = Depends(get_db)):
    new_category = mod_category.Category(**category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/categorys", response_model=List[sch_category.CategoryGet])
def get_categorys(db: Session = Depends(get_db)):
    categorys = db.query(mod_category.Category).all()

    return categorys


@router.get("/category/{id}", response_model=sch_category.Category)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(mod_category.Category).filter(mod_category.Category.id == id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return category


@router.put("/category/{id}", response_model=sch_category.Category)
def update_category(id: int, updated_category: sch_category.Category, db: Session = Depends(get_db)):

    category_query = db.query(mod_category.Category).filter(mod_category.Category.id == id)
    category = category_query.first()

    if category == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    category_query.update(updated_category.dict(), synchronize_session=False)

    db.commit()
    return category_query.first()


@router.delete("/category/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):

    category_query = db.query(mod_category.Category).filter(mod_category.Category.id == id)
    post = category_query.first()

    if post == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    category_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)