from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class DepartmentGroup(Base):
    """
    部门分组模型
    """
    __tablename__ = "department_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    departments = relationship("Department", back_populates="group")

class Department(Base):
    """
    部门模型
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # 关联部门分组
    group_id = Column(Integer, ForeignKey("department_groups.id"))
    group = relationship("DepartmentGroup", back_populates="departments")

    # 关联员工
    employees = relationship("Employee", back_populates="department")