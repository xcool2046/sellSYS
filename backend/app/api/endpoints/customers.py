from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ... import models, schemas
from ...crud import crud_customer
from ...database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud_customer.create_customer(db=db, customer=customer)

from ...models.customer import CustomerStatus

@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    company_name: str = None,
    industry: str = None,
    province: str = None,
    city: str = None,
    status: CustomerStatus = None,
    sales_owner_id: int = None,
):
    query = db.query(models.Customer)
    if company_name:
        query = query.filter(models.Customer.company.contains(company_name))
    if industry:
        query = query.filter(models.Customer.industry == industry)
    if province:
        query = query.filter(models.Customer.province == province)
    if city:
        query = query.filter(models.Customer.city == city)
    if status:
        query = query.filter(models.Customer.status == status)
    if sales_owner_id:
        query = query.filter(models.Customer.sales_owner_id == sales_owner_id)
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud_customer.update_customer(db, customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.delete_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.get("/unassigned/", response_model=List[schemas.Customer])
def read_unassigned_customers(db: Session = Depends(get_db)):
    """获取未分配销售的客户列表"""
    customers = db.query(models.Customer).filter(models.Customer.sales_owner_id == None).all()
    return customers