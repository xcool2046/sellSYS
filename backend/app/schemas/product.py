from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# 基础模型
class ProductBase(BaseModel):
    name: str
    code: Optional[str] = None  # 产品代码
    spec: Optional[str] = None  # 型号规格
    unit: Optional[str] = None
    supplier_price: Optional[Decimal] = None  # 供应商报价
    price: Optional[Decimal] = None  # 报价
    commission: Optional[Decimal] = None  # 提成
    description: Optional[str] = None

# 创建模型
class ProductCreate(ProductBase):
    pass

# 更新模型
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None  # 产品代码
    spec: Optional[str] = None  # 型号规格
    unit: Optional[str] = None
    supplier_price: Optional[Decimal] = None  # 供应商报价
    price: Optional[Decimal] = None  # 报价
    commission: Optional[Decimal] = None  # 提成
    description: Optional[str] = None

# 数据库返回模型
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True