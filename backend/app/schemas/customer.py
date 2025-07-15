from pydantic import BaseModel
from typing import Optional, List
from ..models.customer import CustomerStatus

# 基础模型
class CustomerBase(BaseModel):
    name: str
    industry: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    scale: Optional[str] = None
    status: CustomerStatus = CustomerStatus.LEAD

# 创建模型
class CustomerCreate(CustomerBase):
    pass

# 更新模型
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
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

    class Config:
        from_attributes = True