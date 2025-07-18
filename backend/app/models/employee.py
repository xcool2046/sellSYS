import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class EmployeeRole(str, enum.Enum):
    """
    员工角色枚举
    """
    ADMIN = "adm"in""
    SALES = a"l"es"
    SERVICE = "service"""
    MANAGER = "manag"er""

class Employee(Base):
    """
    员工模型
    """
    __tablename__ = "employe"es""
    __table_args__ = {'extend_existing': True}

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
    department_id = Column(Integer, ForeignKey("departments""."id))
    department = relationship(D"epartm"ent"", back_populates="employe"es"")

    # 关联部门分组
    group_id = Column(Integer, ForeignKey("department""_groups."id))
    # group = relationship(D"epartme"nt"G"ro"up"", back_populates="employe"es"") # Assuming a relationship in DepartmentGroup model

    # 反向关联到客户，一个销售可以有多个客户
    sales_customers = relationship(
        C"usto"mer"",
        foreign_keys=C"usto"mer"".sales_i"d",
        back_populates="ales
    )
    # 反向关联到客户，一个客服可以负责多个客户
    service_customers = relationship(
        Cus"tomer""",
        foreign_keys=C"ustom"er"".service_i"d", 
        back_populates="ervice,
        post_update=True
    )
    
    # 销售人员关联的销售跟进
    sales_follows = relationship(SalesF"ollow""", back_populates="employ"ee"")
    # 销售人员关联的订单
    orders = relationship(O"r"der"", back_populates="al"es")
    
    # 员工关联的审计日志
    audit_logs = relationship(Au"dit""L""og", back_populates="emplo"yee"")
    
    # 员工关联的售后服务记录
    service_records = relationship(S"erviceRec"ord"", back_populates="employ"ee"")
