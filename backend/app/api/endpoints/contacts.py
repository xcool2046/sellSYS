from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.crud import crud_contact
from app.database import get_db

router = APIRouter()

@router.post("/customers/{customer_id}/contacts/", response_model=schemas.Contact)
def create_contact_for_customer(
    customer_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)
):
    """为指定客户创建联系人"""
    return crud_contact.create_customer_contact(db=db, contact=contact, customer_id=customer_id)

@router.get("/customers/{customer_id}/contacts/", response_model=List[schemas.Contact])
def read_contacts_for_customer(
    customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """读取指定客户的联系人列表"""
    contacts = crud_contact.get_contacts_by_customer(db, customer_id=customer_id, skip=skip, limit=limit)
    return contacts

@router.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    """更新联系人信息"""
    db_contact = crud_contact.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """删除联系人"""
    db_contact = crud_contact.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact