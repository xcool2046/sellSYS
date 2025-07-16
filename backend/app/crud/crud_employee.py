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
        name=employee.name,
        email=employee.email,
        hashed_password=hashed_password,
        role=employee.role
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_in: employee_schema.EmployeeUpdate):
    """更新员工信息"""
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        return None
    
    update_data = employee_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    """删除员工"""
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        return None
    db.delete(db_employee)
    db.commit()
    return db_employee