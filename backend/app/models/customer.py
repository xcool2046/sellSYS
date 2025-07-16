import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class CustomerStatus(str, enum.Enum):
    """客户状态"""
    LEAD = "潜在客户"
    CONTACTED = "已联系"
    PROPOSAL = "已报价"
    WON = "成交客户"
    LOST = "流失客户"

class Customer(Base):
    """客户模型"""
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    industry = Column(String) # 行业
    province = Column(String) # 省份
    city = Column(String) # 城市
    address = Column(String) # 详细地址
    website = Column(String) # 公司网站
    scale = Column(String) # 公司规模
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.LEAD)
    
    # 关联销售负责人
    sales_owner_id = Column(Integer, ForeignKey("employees.id"))
    sales_owner = relationship("Employee", foreign_keys=[sales_owner_id], back_populates="sales_customers")
    
    # 关联客服负责人
    service_owner_id = Column(Integer, ForeignKey("employees.id"))
    service_owner = relationship("Employee", foreign_keys=[service_owner_id], back_populates="service_customers")

    # 关联联系人
    contacts = relationship("Contact", back_populates="customer")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Contact(Base):
    """联系人模型"""
    __tablename__ = "contacts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String) # 职位
    phone = Column(String, nullable=False)
    email = Column(String)
    notes = Column(Text) # 备注

    # 关联客户
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="contacts")