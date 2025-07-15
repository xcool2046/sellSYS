from sqlalchemy.orm import Session
from .. import models
from ..schemas import customer as customer_schema

def get_customer(db: Session, customer_id: int):
    """通过ID获取客户"""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """获取客户列表"""
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: customer_schema.CustomerCreate):
    """创建新客户"""
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: customer_schema.CustomerUpdate):
    """更新客户信息"""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    """删除客户"""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer