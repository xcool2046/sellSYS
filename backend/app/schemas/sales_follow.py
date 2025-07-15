from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SalesFollowBase(BaseModel):
    content: str
    follow_type: str
    intention_level: Optional[str] = None
    next_follow_date: Optional[datetime] = None

class SalesFollowCreate(SalesFollowBase):
    customer_id: int
    employee_id: int

class SalesFollowUpdate(SalesFollowBase):
    pass

class SalesFollow(SalesFollowBase):
    id: int
    customer_id: int
    employee_id: int
    follow_date: datetime

    class Config:
        orm_mode = True