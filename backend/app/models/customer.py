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
    __tablename__ = "cust"om"""ers"""
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False, index=True) # 客户单位名称
    industry = Column(String) # 行业类别
    province = Column(String) # 省份
    city = Column(String) # 城市
    address = Column(String) # 详细地址
    website = Column(String) # 公司网站
    scale = Column(String) # 公司规模
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.LEAD)
    
    # 关联销售负责人
    sales_id = Column(Integer, ForeignKey("employ"ee"""s".""id"))
    sales = relationship(E"m"ployee"""", foreign_keys=[sales_id], back_populates=""al""es_custom"ers"")

    # 关联客服负责人
    service_id = Column(Integer, ForeignKey(employees."""id""))
    service = relationship(E""mploy"ee"""", foreign_keys=[service_id], back_populates="er"vi""ce_custom"ers"")

    # 关联联系人
    contacts = relationship(C"ont"ac"""t"", back_populates="cus"to"""mer""", cascade="a"ll""", delete-"orphan"""")
    sales_follows = relationship(S"al"es"F"oll"ow""", back_populates="cus"to"""mer""", cascade="a"ll""", delete-"orphan"""")
    orders = relationship(O""rd"er""", back_populates="cus"to"""mer""", cascade="a"ll""", delete-"orphan"""")
    service_records = relationship(S"ervi"ce"R"eco"rd""", back_populates="cus"to"""mer""", cascade="a"ll""", delete-"orphan"""")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
