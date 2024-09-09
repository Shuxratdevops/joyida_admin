from typing import Optional, List
from src.schemas import sch_categories
from src.models import mod_categories
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from src.db.database import get_db, engine


router = APIRouter(
    # prefix="/",
    tags=["category"]
)


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=sch_categories.Categories)
def create_categories(categories: sch_categories.Categories, db: Session = Depends(get_db)):
    new_categories = mod_categories.Categories(**categories.dict())

    db.add(new_categories)
    db.commit()
    db.refresh(new_categories)

    return new_categories


@router.get("/categories", response_model=List[sch_categories.CategoriesGet])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(mod_categories.Categories).all()

    return categories


@router.get("/categories/{id}", response_model=sch_categories.Categories)
def get_categories(id: int, db: Session = Depends(get_db)):
    categories = db.query(mod_categories.Categories).filter(mod_categories.Categories.id == id).first()

    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return categories


@router.put("/categories/{id}", response_model=sch_categories.Categories)
def update_categories(id: int, updated_categories: sch_categories.Categories, db: Session = Depends(get_db)):

    categories_query = db.query(mod_categories.Categories).filter(mod_categories.Categories.id == id)
    categories = categories_query.first()

    if categories == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    categories_query.update(updated_categories.dict(), synchronize_session=False)

    db.commit()
    return categories_query.first()


@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):

    categories_query = db.query(mod_categories.Categories).filter(mod_categories.Categories.id == id)
    categories = categories_query.first()

    if categories == None:  # so'ralgan id yo'q bo'lsa hato bermaslik uschun
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")


    categories_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)