from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from ..models.order import OrderStatus

# 订单项
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    # unit_price is removed as it should be fetched from the database
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    unit_price: Decimal # The actual price is stored and returned



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
    paid_amount: Optional[Decimal] = None
    total_amount: Decimal
    payment_date: Optional[datetime] = None
    order_items: List[OrderItem] = []
    
    class Config:
        from_attributes = True

# For updating financial info
class OrderFinancialUpdate(BaseModel):
    status: OrderStatus
    paid_amount: Decimal
    payment_date: datetime