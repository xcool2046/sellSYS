from sqlalchemy.orm import Session
from .. import models
from ..schemas import order as order_schema
import uuid
from decimal import Decimal

def get_order(db: Session, order_id: int):
    """获取单个订单"""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """获取订单列表"""
    return db.query(models.Order).offset(skip).limit(limit).all()

def update_order_financials(db: Session, order_id: int, financials: order_schema.OrderFinancialUpdate):
    """更新订单的财务信息"""
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = financials.status
        db_order.paid_amount = financials.paid_amount
        db_order.payment_date = financials.payment_date
        db.commit()
        db.refresh(db_order)
    return db_order

def create_order(db: Session, order: order_schema.OrderCreate):
    """创建新订单"""
    
    total_amount = sum(item.quantity * item.unit_price for item in order.order_items)
    
    db_order = models.Order(
        order_number=str(uuid.uuid4()),
        customer_id=order.customer_id,
        sales_id=order.sales_id,
        total_amount=total_amount,
        status=order.status
    )
    db.add(db_order)
    db.flush() # 使用 flush 来获取订单ID，以便创建订单项

    for item_data in order.order_items:
        db_item = models.OrderItem(
            **item_data.model_dump(),
            order_id=db_order.id
        )
        db.add(db_item)
        
    db.commit()
    db.refresh(db_order)
    return db_order