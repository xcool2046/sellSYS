from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from ..models.customer import CustomerStatus
from .contact import Contact, ContactCreateForCustomer

# 基础模型
class CustomerBase(BaseModel):
    company: str
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    scale: Optional[str] = None
    status: CustomerStatus = CustomerStatus.LEAD

# 创建模型
class CustomerCreate(CustomerBase):
    contacts: List[ContactCreateForCustomer] = []

# 更新模型
class CustomerUpdate(BaseModel):
    company: Optional[str] = None
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    scale: Optional[str] = None
    status: Optional[CustomerStatus] = None
    sales_owner_id: Optional[int] = None
    service_owner_id: Optional[int] = None

# 数据库返回模型
class Customer(CustomerBase):
    id: int
    sales_owner_id: Optional[int] = None
    service_owner_id: Optional[int] = None
    sales_owner_name: Optional[str] = None
    service_owner_name: Optional[str] = None
    contacts: List[Contact] = []
    
    model_config = ConfigDict(from_attributes=True)