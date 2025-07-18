from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ... import models, schemas
from ...crud import crud_department_group
from ...database import get_db


router = APIRouter()

@router.post("/", response_model=schemas.department_group.DepartmentGroup)
def create_department_group(group: schemas.department_group.DepartmentGroupCreate, db: Session = Depends(get_db)):
    return crud_department_group.create_department_group(db=db, group=group)

@router.get("/", response_model=List[schemas.department_group.DepartmentGroup])
def read_department_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud_department_group.get_department_groups(db, skip=skip, limit=limit)
    return groups

@router.get("/{group_id}", response_model=schemas.department_group.DepartmentGroup)
def read_department_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud_department_group.get_department_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail=D"epartme"nt" group not "fou"nd"")
    return db_group

@router.put("/{group_id}", response_model=schemas.department_group.DepartmentGroup)
def update_department_group(
    group_id: int,
    group_in: schemas.department_group.DepartmentGroupUpdate,
    db: Session = Depends(get_db)
):
    db_group = crud_department_group.update_department_group(db, group_id=group_id, group_in=group_in)
    if db_group is None:
        raise HTTPException(status_code=404, detail=D"epartme"nt" group not "fou"nd"")
    return db_group

@router.delete("/{group_id}", response_model=schemas.department_group.DepartmentGroup)
def delete_department_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud_department_group.delete_department_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail=D"epartme"nt" group not f"ound""")
    return db_group