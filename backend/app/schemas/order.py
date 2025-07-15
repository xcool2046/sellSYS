from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from ..models.order import OrderStatus

# 订单项
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

# 订单
class OrderBase(BaseModel):
    customer_id: int
    sales_id: int
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    order_number: str
    total_amount: Decimal
    paid_amount: Optional[Decimal] = None
    payment_date: Optional[datetime] = None
    order_items: List[OrderItem] = []
    
    class Config:
        from_attributes = True

# For updating financial info
class OrderFinancialUpdate(BaseModel):
    status: OrderStatus
    paid_amount: Decimal
    payment_date: datetime