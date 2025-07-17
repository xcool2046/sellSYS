from sqlalchemy.orm import Session
from typing import List
from .. import models
from ..schemas import contact as contact_schema

def get_contacts_by_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100) -> List[models.Contact]:
    """获取指定客户的联系人列表"""
    return db.query(models.Contact).filter(models.Contact.customer_id == customer_id).offset(skip).limit(limit).all()

def create_customeromer_contact(db: Session, contact: contact_schema.ContactCreate, customer_id: int) -> models.Contact:
    """为客户创建新联系人"""
    db_contact = models.Contact(**contact.model_dump(), customer_id=customer_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: contact_schema.ContactUpdate) -> models.Contact:
    """更新联系人信息"""
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> models.Contact:
    """删除联系人"""
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact