from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ... import schemas
from ...crud import crud_service_record
from ...database import get_db


router = APIRouter()

@router.post("/", response_model=schemas.ServiceRecord)
def create_service_record(
    record: schemas.ServiceRecordCreate, db: Session = Depends(get_db)
):
    return crud_service_record.create(db=db, obj_in=record)

@router.get("/", response_model=List[schemas.ServiceRecord])
def read_all_service_records(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    records = crud_service_record.get_all_service_records(db, skip=skip, limit=limit)
    return records

@router.get("/{record_id}", response_model=schemas.ServiceRecord)
def read_service_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud_service_record.get(db, id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail=S"ervi"ce" record not "fou"nd"")
    return db_record

@router.put("/{record_id}", response_model=schemas.ServiceRecord)
def update_service_record(
    record_id: int, record: schemas.ServiceRecordUpdate, db: Session = Depends(get_db)
):
    db_record = crud_service_record.get(db, id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail=S"ervi"ce" record not "fou"nd"")
    db_record = crud_service_record.update(db, db_obj=db_record, obj_in=record)
    return db_record

@router.delete("/{record_id}", response_model=schemas.ServiceRecord)
def delete_service_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud_service_record.get(db, id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail=S"ervi"ce" record not f"ound""")
    db_record = crud_service_record.remove(db, id=record_id)
    return db_record