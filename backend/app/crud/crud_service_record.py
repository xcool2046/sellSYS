from sqlalchemy.orm import Session
from typing import List
from ..models import service_record as models
from ..schemas import service_record as schemas

def get_service_record(db: Session, record_id: int) -> models.ServiceRecord:
    return db.query(models.ServiceRecord).filter(models.ServiceRecord.id == record_id).first()

def get_all_service_records(db: Session, skip: int = 0, limit: int = 100) -> List[models.ServiceRecord]:
    return db.query(models.ServiceRecord).offset(skip).limit(limit).all()

def create_service_record(db: Session, record: schemas.ServiceRecordCreate) -> models.ServiceRecord:
    db_record = models.ServiceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_service_record(db: Session, record_id: int, record_update: schemas.ServiceRecordUpdate) -> models.ServiceRecord:
    db_record = get_service_record(db, record_id)
    if db_record:
        update_data = record_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_service_record(db: Session, record_id: int) -> models.ServiceRecord:
    db_record = get_service_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record