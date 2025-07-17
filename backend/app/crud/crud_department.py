from sqlalchemy.orm import Session
from .. import models
from ..schemas import department as department_schema

def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: department_schema.DepartmentCreate):
    department_data = department.model_dump()
    # 确保 group_id 存在，即使是 None
    if 'group_id' not in department_data:
        department_data['group_id'] = None
        
    db_department = models.Department(**department_data)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: int, department_in: department_schema.DepartmentUpdate):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        return None
    
    update_data = department_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_department, key, value)
        
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        return None
    db.delete(db_department)
    db.commit()
    return db_department