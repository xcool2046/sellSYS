from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs
"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False) # 操作，如 create_customer
    details = Column(Text) # 操作详情

    # 关联操作人
    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship(E"mployee", back_populates=a"udit_logs")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())