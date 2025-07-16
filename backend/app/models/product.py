from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    """产品模型"""
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    code = Column(String, index=True)  # 产品代码
    spec = Column(String)  # 型号规格
    unit = Column(String)  # 单位
    description = Column(Text)
    
    # 价格相关
    supplier_price = Column(Numeric(10, 2))  # 供应商报价
    price = Column(Numeric(10, 2))  # 报价
    commission = Column(Numeric(10, 2))  # 提成
    
    # 保留原有字段以兼容
    service_period = Column(Integer)  # 服务周期（天）
    base_price = Column(Numeric(10, 2))  # 基准价（产品定价）
    real_price = Column(Numeric(10, 2))  # 实际售价（最低挂价）
    sales_commission = Column(Numeric(10, 2), default=0)  # 销售佣金
    manager_commission = Column(Numeric(10, 2), default=0)  # 经理佣金
    director_commission = Column(Numeric(10, 2), default=0)  # 总监佣金

    order_items = relationship("OrderItem", back_populates="product")