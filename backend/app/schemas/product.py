from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# 基础模型
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    commission_rate: Optional[Decimal] = 0

# 创建模型
class ProductCreate(ProductBase):
    pass

# 更新模型
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    commission_rate: Optional[Decimal] = None

# 数据库返回模型
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True