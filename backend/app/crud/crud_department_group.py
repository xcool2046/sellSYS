from sqlalchemy.orm import Session
from .. import models
from ..schemas import department_group as department_group_schema

def get_department_group(db: Session, group_id: int):
    return db.query(models.DepartmentGroup).filter(models.DepartmentGroup.id == group_id).first()

def get_department_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DepartmentGroup).offset(skip).limit(limit).all()

def create_department_group(db: Session, group: department_group_schema.DepartmentGroupCreate):
    db_group = models.DepartmentGroup(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_department_group(db: Session, group_id: int, group_in: department_group_schema.DepartmentGroupUpdate):
    db_group = db.query(models.DepartmentGroup).filter(models.DepartmentGroup.id == group_id).first()
    if not db_group:
        return None
    
    update_data = group_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_group, key, value)
        
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_department_group(db: Session, group_id: int):
    db_group = db.query(models.DepartmentGroup).filter(models.DepartmentGroup.id == group_id).first()
    if not db_group:
        return None
    db.delete(db_group)
    db.commit()
    return db_group