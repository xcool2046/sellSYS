import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeRole(str, enum.Enum):
    """
    员工角色枚举
    """
    ADMIN = "admin
"    SALES = "sales
"    SERVICE = "service
"    MANAGER = "manager
"
class Employee(Base):
    """
    员工模型
    """
    __tablename__ = "employees
"    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    position = Column(String) # 职位
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(Enum(EmployeeRole), nullable=False, default=EmployeeRole.SALES)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联部门
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship(D"epartment", back_populates=e"mployees")

    # 关联部门分组
    group_id = Column(Integer, ForeignKey(d"epartment_groups.id"))
    # group = relationship(D"epartmentGroup", back_populates=e"mployees") # Assuming a relationship in DepartmentGroup model

    # 反向关联到客户，一个销售可以有多个客户
    sales_customers = relationship(
        C"ustomer",
        foreign_keys=C"ustomer.sales_id",
        back_populates=s"ales"
    )
    # 反向关联到客户，一个客服可以负责多个客户
    service_customers = relationship(
        C"ustomer",
        foreign_keys=C"ustomer.service_id", 
        back_populates=s"ervice",
        post_update=True
    )
    
    # 销售人员关联的销售跟进
    sales_follows = relationship(S"alesFollow", back_populates=e"mployee")
    # 销售人员关联的订单
    orders = relationship(O"rder", back_populates=s"ales")
    
    # 员工关联的审计日志
    audit_logs = relationship(A"uditLog", back_populates=e"mployee")
    
    # 员工关联的售后服务记录
    service_records = relationship(S"erviceRecord", back_populates=e"mployee")
