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
