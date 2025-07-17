from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceRecordBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Open
"
class ServiceRecordCreate(ServiceRecordBase):
    customer_id: int
    employee_id: int # The employee who is assigned to this record

class ServiceRecordUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    employee_id: Optional[int] = None

class ServiceRecord(ServiceRecordBase):
    id: int
    customer_id: int
    employee_id: int
    created_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True