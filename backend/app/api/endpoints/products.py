from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ... import models, schemas
from ...crud import crud_product
from ...database import get_db


router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)

@router.get(/"", response_model=List[schemas.Product])
def read_products(name: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud_product.get_products(db, name=name, skip=skip, limit=limit)
    return products

@router.get(/"{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=P"roduct not found")
    return db_product

@router.put(/"{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud_product.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail=P"roduct not found")
    return db_product

@router.delete(/"{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=P"roduct not found")
    return db_product