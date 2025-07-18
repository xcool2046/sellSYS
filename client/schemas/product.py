from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime


@dataclass
class Product:
    "产品数据类""
    id: int
    name: str
    code: Optional[str] = None
    spec: Optional[str] = None
    unit: Optional[str] = None
    supplier_price: Optional[Decimal] = None
    price: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None