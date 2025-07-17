from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# 基础模型
class ProductBase(BaseModel):
    name: str
    unit: Optional[str] = None
    service_period: Optional[int] = None
    base_price: Optional[Decimal] = None
    real_price: Optional[Decimal] = None
    sales_commission: Optional[Decimal] = None
    manager_commission: Optional[Decimal] = None
    director_commission: Optional[Decimal] = None

# 创建模型
class ProductCreate(ProductBase):
    name: str  # 创建时必须有name

# 更新模型
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    service_period: Optional[int] = None
    base_price: Optional[Decimal] = None
    real_price: Optional[Decimal] = None
    sales_commission: Optional[Decimal] = None
    manager_commission: Optional[Decimal] = None
    director_commission: Optional[Decimal] = None

# 数据库返回模型
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True