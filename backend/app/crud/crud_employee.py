from sqlalchemy.orm import Session
from .. import models
from ..schemas import employee as employee_schema
from ..core.security import get_password_hash

def get_employee_by_username(db: Session, username: str):
    """通过用户名获取员工"""
    return db.query(models.Employee).filter(models.Employee.username == username).first()

def create_employee(db: Session, employee: employee_schema.EmployeeCreate):
    """创建新员工"""
    hashed_password = get_password_hash(employee.password)
    db_employee = models.Employee(
        username=employee.username,
        full_name=employee.full_name,
        email=employee.email,
        hashed_password=hashed_password,
        role=employee.role
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee