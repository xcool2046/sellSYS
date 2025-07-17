from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    """产品模型"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    unit = Column(String)
    service_period = Column(Integer)  # 服务周期（天）
    base_price = Column(Numeric(10, 2))  # 基准价
    real_price = Column(Numeric(10, 2))  # 实际售价
    sales_commission = Column(Numeric(10, 2), default=0.0)  # 销售佣金
    manager_commission = Column(Numeric(10, 2), default=0.0)  # 经理佣金
    director_commission = Column(Numeric(10, 2), default=0.0)  # 总监佣金

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")