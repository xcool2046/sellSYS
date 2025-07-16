import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class OrderStatus(str, enum.Enum):
    """订单状态"""
    PENDING = "待付款"
    PAID = "已付款"
    PROCESSING = "处理中"
    SHIPPED = "已发货"
    COMPLETED = "已完成"
    CANCELED = "已取消"
    PARTIALLY_PAID = "部分付款"

class Order(Base):
    """订单模型"""
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0.0)
    payment_date = Column(DateTime, nullable=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    start_date = Column(DateTime, nullable=True) # 服务开始日期
    end_date = Column(DateTime, nullable=True) # 服务结束日期
    
    # 关联客户
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    
    # 关联销售
    sales_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    sales = relationship("Employee", back_populates="orders")
    
    order_items = relationship("OrderItem", back_populates="order")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OrderItem(Base):
    """订单项模型"""
    __tablename__ = "order_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # 关联订单
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="order_items")
    
    # 关联产品
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="order_items")