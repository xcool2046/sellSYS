from sqlalchemy.orm import Session
from .. import models
from ..schemas import customer as customer_schema

def get_customeromer(db: Session, customer_id: int):
    """通过ID获取客户"""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customeromers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    company: str = None,
    industry: str = None,
    province: str = None,
    city: str = None,
    status: str = None,
    sales_id: int = None,
):
    """获取客户列表并根据条件过滤"""
    query = db.query(models.Customer)

    if company:
        query = query.filter(models.Customer.company.contains(company))
    if industry:
        query = query.filter(models.Customer.industry.contains(industry))
    if province:
        query = query.filter(models.Customer.province == province)
    if city:
        query = query.filter(models.Customer.city == city)
    if status:
        query = query.filter(models.Customer.status == status)
    if sales_id:
        query = query.filter(models.Customer.sales_id == sales_id)

    return query.offset(skip).limit(limit).all()

def create_customeromer(db: Session, customer: customer_schema.CustomerCreate):
    """创建新客户（包括联系人）"""
    customer_data = customer.model_dump(exclude={"contacts"})
    db_customer = models.Customer(**customer_data)
    
    # 创建联系人
    for contact_data in customer.contacts:
        db_contact = models.Contact(**contact_data.model_dump())
        db_customer.contacts.append(db_contact)
        
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customeromer(db: Session, customer_id: int, customer: customer_schema.CustomerUpdate):
    """更新客户信息"""
    db_customer = get_customeromer(db, customer_id)
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customeromer(db: Session, customer_id: int):
    """删除客户"""
    db_customer = get_customeromer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer