from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.crud import crud_order
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """创建新订单"""
    return crud_order.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """读取订单列表"""
    orders = crud_order.get_orders(db, skip=skip, limit=limit)
    return orders

@router.put("/{order_id}/financials", response_model=schemas.Order)
def update_order_financials(
    order_id: int,
    financials: schemas.OrderFinancialUpdate,
    db: Session = Depends(get_db)
):
    """更新订单的财务信息（收款状态、金额、日期）"""
    db_order = crud_order.update_order_financials(
        db, order_id=order_id, financials=financials
    )
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order