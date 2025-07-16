from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.crud import crud_sales_follow
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.SalesFollow)
def create_sales_follow(
    follow: schemas.SalesFollowCreate, db: Session = Depends(get_db)
):
    return crud_sales_follow.create_sales_follow(db=db, follow=follow)

@router.get("/customer/{customer_id}", response_model=List[schemas.SalesFollow])
def read_sales_follows_by_customer(
    customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    follows = crud_sales_follow.get_sales_follows_by_customer(
        db, customer_id=customer_id, skip=skip, limit=limit
    )
    return follows

@router.get("/{follow_id}", response_model=schemas.SalesFollow)
def read_sales_follow(follow_id: int, db: Session = Depends(get_db)):
    db_follow = crud_sales_follow.get_sales_follow(db, follow_id=follow_id)
    if db_follow is None:
        raise HTTPException(status_code=404, detail="Sales follow not found")
    return db_follow

@router.put("/{follow_id}", response_model=schemas.SalesFollow)
def update_sales_follow(
    follow_id: int, follow: schemas.SalesFollowUpdate, db: Session = Depends(get_db)
):
    db_follow = crud_sales_follow.update_sales_follow(db, follow_id=follow_id, follow_update=follow)
    if not db_follow:
        raise HTTPException(status_code=404, detail="Sales follow not found")
    return db_follow

@router.delete("/{follow_id}", response_model=schemas.SalesFollow)
def delete_sales_follow(follow_id: int, db: Session = Depends(get_db)):
    db_follow = crud_sales_follow.delete_sales_follow(db, follow_id=follow_id)
    if not db_follow:
        raise HTTPException(status_code=404, detail="Sales follow not found")
    return db_follow