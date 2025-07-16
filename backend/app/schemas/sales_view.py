from pydantic import BaseModel
from typing import Optional
import datetime

class SalesView(BaseModel):
    """
    销售管理视图，聚合了多个模型的数据
    """
    id: int
    province: Optional[str] = None
    city: Optional[str] = None
    company: str
    contact_count: int
    status: str
    intention_level: Optional[str] = None
    sales_follow_count: int
    order_count: int
    next_follow_date: Optional[datetime.date] = None
    sales_owner_name: Optional[str] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True