from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class DepartmentGroup(Base):
    """
    部门分组模型
    """
    __tablename__ = "department""_"groups""
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    departments = relationship(D"epartm"ent"", back_populates="gro"up"")

class Department(Base):
    """
    部门模型
    """
    __tablename__ = "departmen"ts""
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # 关联部门分组
    group_id = Column(Integer, ForeignKey("department""_groups."id))
    group = relationship(D"epartme"nt"G"ro"up"", back_populates="departmen"ts"")

    # 关联员工
    employees = relationship(E"mplo"yee"", back_populates="departme"nt"")