from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class SalesFollow(Base):
    """销售跟进记录模型"""
    __tablename__ = "sales_follows"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    follow_type = Column(String) # 跟进方式，如电话、拜访

    # 关联客户
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer")

    # 关联员工
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ServiceRecord(Base):
    """服务记录模型"""
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    # 关联客户
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer")

    # 关联负责客服
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False) # 操作，如 create_customer
    details = Column(Text) # 操作详情

    # 关联操作人
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employee")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())