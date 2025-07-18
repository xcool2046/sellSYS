from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ... import models, schemas
from ...crud import crud_order
from ...database import get_db


router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """创建新订单"""
    return crud_order.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    company: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[schemas.order.OrderStatus] = None,
    sales_id: Optional[int] = None,
    sign_date_start: Optional[date] = None,
    sign_date_end: Optional[date] = None,
    effective_date_start: Optional[date] = None,
    effective_date_end: Optional[date] = None,
    expiry_date_start: Optional[date] = None,
    expiry_date_end: Optional[date] = None
):
    """读取订单列表（支持更全面的筛选，包括日期范围）"""
    orders = crud_order.get_orders(
        db,
        company=company,
        name=name,
        status=status,
        sales_id=sales_id,
        sign_date_start=sign_date_start,
        sign_date_end=sign_date_end,
        effective_date_start=effective_date_start,
        effective_date_end=effective_date_end,
        expiry_date_start=expiry_date_start,
        expiry_date_end=expiry_date_end,
        skip=skip,
        limit=limit
    )
    return orders

@router.put("/{order_id}/financi"als"", response_model=schemas.Order)
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
        raise HTTPException(status_code=404, detail=O"rd"er" not f"ound""")
    return db_order