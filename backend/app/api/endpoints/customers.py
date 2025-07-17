from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ... import models, schemas
from ...crud import crud_customer
from ...database import get_db
from ...models.customer import CustomerStatus
from ...crud import crud_contact


router = APIRouter()

@router.post("/", response_model=schemas.Customer)
def create_customeromer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud_customer.create_customeromer(db=db, customer=customer)


@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    company: str = None,
    industry: str = None,
    province: str = None,
    city: str = None,
    status: CustomerStatus = None,
    sales_id: int = None,
):
    customers = crud_customer.get_customeromers(
        db,
        skip=skip,
        limit=limit,
        company=company,
        industry=industry,
        province=province,
        city=city,
        status=status,
        sales_id=sales_id,
    )
    
    # Manually assemble the response to include owner names
    response_customers = []
    for customer in customers:
        customer_data = schemas.Customer.from_orm(customer).dict()
        customer_data['sales_owner_name'] = customer.sales.full_name if customer.sales else None
        customer_data['service_owner_name'] = customer.service.full_name if customer.service else None
        response_customers.append(customer_data)
        
    return response_customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customeromer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customeromer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud_customer.update_customeromer(db, customer_id=customer_id, customer=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customeromer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.delete_customeromer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.get("/unassigned/", response_model=List[schemas.Customer])
def read_unassigned_customers(db: Session = Depends(get_db)):
    """获取未分配销售的客户列表"""
    customers = db.query(models.Customer).filter(models.Customer.sales_id == None).all()
    return customers


@router.get("/{customer_id}/contacts/", response_model=List[schemas.Contact])
def read_customer_contacts(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve contacts for a specific customer.
    """
    contacts = crud_contact.get_contacts_by_customer(db, customer_id=customer_id)
    return contacts