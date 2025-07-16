import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeRole(str, enum.Enum):
    """
    员工角色枚举
    """
    ADMIN = "admin"
    SALES = "sales"
    SERVICE = "service"
    MANAGER = "manager"

class Employee(Base):
    """
    员工模型
    """
    __tablename__ = "employees"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(Enum(EmployeeRole), nullable=False, default=EmployeeRole.SALES)
    is_active = Column(Boolean, default=True)
    
    # 关联部门
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")

    # 反向关联到客户，一个销售可以有多个客户
    sales_customers = relationship(
        "Customer",
        foreign_keys="[Customer.sales_owner_id]",
        back_populates="sales_owner"
    )
    # 反向关联到客户，一个客服可以负责多个客户
    service_customers = relationship(
        "Customer",
        foreign_keys="[Customer.service_owner_id]",
        back_populates="service_owner"
    )
