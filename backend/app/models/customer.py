import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime, Boolean
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
    company = Column(String, nullable=False, index=True)  # 客户单位名称
    industry = Column(String)  # 行业类别
    province = Column(String)  # 省份
    city = Column(String)  # 城市
    address = Column(String)  # 详细地址
    website = Column(String)  # 公司网站
    scale = Column(String)  # 公司规模
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.LEAD)
    notes = Column(Text)  # 客户备注

    # 关联销售负责人
    sales_id = Column(Integer, ForeignKey("employees.id"))
    # sales = relationship("Employee", foreign_keys=[sales_id], back_populates="sales_customers")

    # 关联客服负责人
    service_id = Column(Integer, ForeignKey("employees.id"))
    # service = relationship("Employee", foreign_keys=[service_id], back_populates="service_customers")

    # 关联联系人
    # contacts = relationship("Contact", back_populates="customer", cascade="all, delete-orphan")
    # sales_follows = relationship("SalesFollow", back_populates="customer", cascade="all, delete-orphan")
    # orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    # service_records = relationship("ServiceRecord", back_populates="customer", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
